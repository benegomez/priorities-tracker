from datetime import date, datetime

from pydantic import BaseModel


class TeamSummaryRequest(BaseModel):
    regenerate: bool = False


class DataSnapshot(BaseModel):
    team_size: int
    week_start: str
    avg_crs: float
    total_priorities: int
    completed_priorities: int
    completion_rate: float


class TeamSummaryResponse(BaseModel):
    summary: str
    generated_at: datetime
    model: str | None
    data_snapshot: DataSnapshot
    fallback: bool
    cached: bool
