from typing import Optional

from pydantic import BaseModel, Field


class RouteRequest(BaseModel):
    query: str = Field(..., min_length=1, description="User query to route")


class RouteResponse(BaseModel):
    query_id: int
    query: str
    route: str
    response: str
    confidence_score: float
    classifier_label: str
    heuristic_route: Optional[str] = None
    latency_ms: float
    estimated_cost: float
    estimated_energy: float


class FeedbackRequest(BaseModel):
    query_id: int
    rating: int = Field(..., ge=1, le=5)
    comments: Optional[str] = None
    correct_route: Optional[str] = None

