from fastapi import APIRouter, HTTPException
from db.models import RouteRequest, RouteResponse, FeedbackRequest
from core.router import process_and_route
from db.database import get_db_connection

router = APIRouter()

@router.post("/route", response_model=RouteResponse)
async def route_query(request: RouteRequest):
    try:
        result = process_and_route(request.query)
        return RouteResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/feedback")
async def submit_feedback(request: FeedbackRequest):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO feedback (query_id, rating, comments)
        VALUES (?, ?, ?)
    ''', (request.query_id, request.rating, request.comments))
    conn.commit()
    conn.close()
    return {"status": "success", "message": "Feedback submitted successfully"}

@router.get("/analytics")
async def get_analytics(limit: int = 100):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id, query, route, latency_ms, estimated_cost, estimated_energy, timestamp
        FROM queries
        ORDER BY timestamp DESC
        LIMIT ?
    ''', (limit,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

@router.get("/cost-summary")
async def get_cost_summary():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT route, SUM(estimated_cost) as total_cost, COUNT(*) as query_count
        FROM queries
        GROUP BY route
    ''')
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

@router.get("/energy-summary")
async def get_energy_summary():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT route, SUM(estimated_energy) as total_energy, COUNT(*) as query_count
        FROM queries
        GROUP BY route
    ''')
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

@router.get("/health")
async def health_check():
    return {"status": "ok"}
