from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel


class CRSCurrentResponse(BaseModel):
    score: float
    trend: str
    risk_level: str
    week_start: date
    formula_version: str
    priorities_total: int
    priorities_completed: int
    tasks_total: int
    tasks_completed: int


class CRSHistoryItem(BaseModel):
    week_start: date
    score: float
    trend: str
    risk_level: str


class CRSHistoryResponse(BaseModel):
    items: list[CRSHistoryItem]
