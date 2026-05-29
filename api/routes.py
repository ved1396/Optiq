import logging

import pandas as pd
from fastapi import APIRouter, HTTPException, Query

from config import settings
from core.analytics_logger import log_feedback
from core.cost_calc import estimate_cost_saved
from core.energy_calc import estimate_energy_saved
from core.router import process_and_route
from db.database import read_dataframe
from db.models import FeedbackRequest, RouteRequest, RouteResponse

logger = logging.getLogger(__name__)
router = APIRouter(tags=["Optiq"])


def _empty_analytics_payload() -> dict:
    return {
        "summary": {
            "total_queries": 0,
            "routing_accuracy": 0.0,
            "average_latency_ms": 0.0,
            "last_updated": None,
        },
        "route_distribution": [],
        "latency_trend": [],
        "recent_queries": [],
    }


@router.post("/route", response_model=RouteResponse)
async def route_query(request: RouteRequest) -> RouteResponse:
    try:
        return RouteResponse(**process_and_route(request.query))
    except Exception as exc:
        logger.exception("Routing failure")
        raise HTTPException(status_code=500, detail=f"Unable to route query: {exc}") from exc


@router.post("/feedback")
async def submit_feedback(request: FeedbackRequest) -> dict:
    try:
        log_feedback(request.query_id, request.rating, request.comments, request.correct_route)
        return {"status": "success", "message": "Feedback stored successfully."}
    except Exception as exc:
        logger.exception("Feedback failure")
        raise HTTPException(status_code=500, detail=f"Unable to save feedback: {exc}") from exc


@router.get("/analytics")
async def get_analytics(limit: int = Query(default=200, ge=1, le=5000)) -> dict:
    df = read_dataframe(
        """
        SELECT q.id, q.query, q.route, q.response, q.latency_ms, q.estimated_cost, q.estimated_energy,
               q.confidence_score, q.classifier_label, q.heuristic_route, q.created_at,
               a.feedback_rating, a.correct_route
        FROM queries q
        LEFT JOIN analytics a ON q.id = a.query_id
        ORDER BY q.created_at DESC
        LIMIT ?
        """,
        (limit,),
    )
    if df.empty:
        return _empty_analytics_payload()

    df["created_at"] = pd.to_datetime(df["created_at"])
    feedback_df = df[df["feedback_rating"].notna()].copy()
    if not feedback_df.empty:
        correctness = (
            (feedback_df["correct_route"].fillna(feedback_df["route"]) == feedback_df["route"])
            | (feedback_df["feedback_rating"] >= 4)
        )
        routing_accuracy = round(float(correctness.mean() * 100), 2)
    else:
        heuristic_correct = df["heuristic_route"].notna() & (df["heuristic_route"] == df["route"])
        classifier_correct = df["heuristic_route"].isna() & (
            df["confidence_score"] >= settings.classifier_confidence_threshold
        )
        routing_accuracy = round(float((heuristic_correct | classifier_correct).mean() * 100), 2)

    route_distribution = (
        df["route"].value_counts().rename_axis("route").reset_index(name="count").to_dict(orient="records")
    )
    latency_trend = (
        df.sort_values("created_at")[["created_at", "latency_ms"]]
        .assign(created_at=lambda frame: frame["created_at"].dt.strftime("%Y-%m-%d %H:%M:%S"))
        .to_dict(orient="records")
    )
    recent_queries = (
        df[["id", "query", "route", "latency_ms", "estimated_cost", "estimated_energy", "created_at"]]
        .assign(created_at=lambda frame: frame["created_at"].dt.strftime("%Y-%m-%d %H:%M:%S"))
        .head(20)
        .to_dict(orient="records")
    )

    return {
        "summary": {
            "total_queries": int(len(df)),
            "routing_accuracy": routing_accuracy,
            "average_latency_ms": round(float(df["latency_ms"].mean()), 2),
            "last_updated": df["created_at"].max().strftime("%Y-%m-%d %H:%M:%S"),
        },
        "route_distribution": route_distribution,
        "latency_trend": latency_trend,
        "recent_queries": recent_queries,
    }


@router.get("/cost-summary")
async def get_cost_summary() -> dict:
    df = read_dataframe(
        """
        SELECT route, estimated_cost, created_at
        FROM queries
        ORDER BY created_at ASC
        """
    )
    if df.empty:
        return {"summary": {"total_cost": 0.0, "estimated_cost_saved": 0.0}, "cost_per_route": [], "historical_trends": []}

    df["created_at"] = pd.to_datetime(df["created_at"])
    route_cost = df.groupby("route", as_index=False)["estimated_cost"].sum()
    route_cost["estimated_saved"] = route_cost.apply(
        lambda row: estimate_cost_saved(row["route"], float(row["estimated_cost"]) / max(len(df[df["route"] == row["route"]]), 1))
        * len(df[df["route"] == row["route"]]),
        axis=1,
    )
    historical = df.copy()
    historical["cumulative_cost"] = historical["estimated_cost"].cumsum()
    historical["baseline_cost"] = settings.baseline_large_llm_cost
    historical["created_at"] = historical["created_at"].dt.strftime("%Y-%m-%d %H:%M:%S")

    total_cost = round(float(df["estimated_cost"].sum()), 6)
    baseline = round(float(len(df) * settings.baseline_large_llm_cost), 6)
    return {
        "summary": {
            "total_cost": total_cost,
            "estimated_cost_saved": round(max(baseline - total_cost, 0.0), 6),
            "baseline_large_llm_cost": baseline,
        },
        "cost_per_route": route_cost.round(6).to_dict(orient="records"),
        "historical_trends": historical[["created_at", "estimated_cost", "cumulative_cost", "baseline_cost"]].to_dict(
            orient="records"
        ),
    }


@router.get("/energy-summary")
async def get_energy_summary() -> dict:
    df = read_dataframe(
        """
        SELECT route, estimated_energy, created_at
        FROM queries
        ORDER BY created_at ASC
        """
    )
    if df.empty:
        return {
            "summary": {"total_energy": 0.0, "estimated_energy_saved": 0.0},
            "energy_per_route": [],
            "historical_trends": [],
        }

    df["created_at"] = pd.to_datetime(df["created_at"])
    route_energy = df.groupby("route", as_index=False)["estimated_energy"].sum()
    route_energy["estimated_saved"] = route_energy.apply(
        lambda row: estimate_energy_saved(row["route"], float(row["estimated_energy"]) / max(len(df[df["route"] == row["route"]]), 1))
        * len(df[df["route"] == row["route"]]),
        axis=1,
    )
    historical = df.copy()
    historical["cumulative_energy"] = historical["estimated_energy"].cumsum()
    historical["baseline_energy"] = settings.baseline_large_llm_energy
    historical["created_at"] = historical["created_at"].dt.strftime("%Y-%m-%d %H:%M:%S")

    total_energy = round(float(df["estimated_energy"].sum()), 3)
    baseline = round(float(len(df) * settings.baseline_large_llm_energy), 3)
    return {
        "summary": {
            "total_energy": total_energy,
            "estimated_energy_saved": round(max(baseline - total_energy, 0.0), 3),
            "baseline_large_llm_energy": baseline,
        },
        "energy_per_route": route_energy.round(3).to_dict(orient="records"),
        "historical_trends": historical[
            ["created_at", "estimated_energy", "cumulative_energy", "baseline_energy"]
        ].to_dict(orient="records"),
    }


@router.get("/health")
async def health_check() -> dict:
    analytics_df = read_dataframe("SELECT route, created_at FROM queries ORDER BY created_at DESC LIMIT 1000")
    total_df = read_dataframe("SELECT COUNT(*) AS total_queries FROM queries")
    route_usage = (
        analytics_df["route"].value_counts().rename_axis("route").reset_index(name="count").to_dict(orient="records")
        if not analytics_df.empty
        else []
    )
    return {
        "status": "ok",
        "database": "connected",
        "total_queries": int(total_df.iloc[0]["total_queries"]) if not total_df.empty else 0,
        "route_usage": route_usage,
        "models": {
            "local_llm": settings.ollama_model,
            "large_llm": settings.openai_model,
            "classifier_threshold": settings.classifier_confidence_threshold,
        },
    }
