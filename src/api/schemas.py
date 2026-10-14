from pydantic import BaseModel
from typing import List, Dict, Any

class RouteMetrics(BaseModel):
    total_distance_meters: float
    total_duration_seconds: float
    average_velocity_kmh: float

class ProcessBatchResponse(BaseModel):
    status: str
    processed_frames: int
    metrics: RouteMetrics
    path_preview: List[Dict[str, Any]]