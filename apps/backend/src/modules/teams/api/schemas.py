from datetime import date
from uuid import UUID

from pydantic import BaseModel


class TeamMemberCRS(BaseModel):
    score: float
    trend: str
    risk_level: str


class TeamMemberWeekStatus(BaseModel):
    week_start: date
    checkin_status: str | None = None
    checkout_status: str | None = None


class TeamMemberItem(BaseModel):
    id: UUID
    first_name: str
    last_name: str
    email: str
    crs: TeamMemberCRS | None = None
    week_status: TeamMemberWeekStatus


class TeamOverviewResponse(BaseModel):
    members: list[TeamMemberItem]


class TeamMemberEmployee(BaseModel):
    id: UUID
    first_name: str
    last_name: str


class TeamMemberCRSCurrent(BaseModel):
    score: float
    trend: str
    risk_level: str
    week_start: date


class CRSHistoryItem(BaseModel):
    week_start: date
    score: float
    trend: str
    risk_level: str


class TeamMemberCRSResponse(BaseModel):
    employee: TeamMemberEmployee
    current: TeamMemberCRSCurrent | None = None
    history: list[CRSHistoryItem]
