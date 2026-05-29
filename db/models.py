from pydantic import BaseModel
from typing import Optional

class RouteRequest(BaseModel):
    query: str

class RouteResponse(BaseModel):
    query_id: int
    query: str
    route: str
    response: str
    confidence_score: float
    latency_ms: float
    estimated_cost: float
    estimated_energy: float

class FeedbackRequest(BaseModel):
    query_id: int
    rating: int
    comments: Optional[str] = None
