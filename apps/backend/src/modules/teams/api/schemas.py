from datetime import date, datetime
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


# ── Admin Team Management schemas ─────────────────────────────────────────────

class TeamCreate(BaseModel):
    name: str
    manager_id: UUID | None = None


class TeamUpdate(BaseModel):
    name: str | None = None
    manager_id: UUID | None = None


class TeamMemberAdd(BaseModel):
    user_id: UUID


class AdminTeamMemberItem(BaseModel):
    id: UUID
    first_name: str
    last_name: str
    role: str
    status: str


class AdminTeamResponse(BaseModel):
    id: UUID
    name: str
    manager_id: UUID | None
    manager_name: str | None
    member_count: int
    created_at: datetime | None = None
    updated_at: datetime | None = None

    model_config = {"from_attributes": True}


class AdminTeamDetailResponse(AdminTeamResponse):
    members: list[AdminTeamMemberItem] = []


class AdminTeamListResponse(BaseModel):
    items: list[AdminTeamResponse]
    total: int
    page: int
    page_size: int
    pages: int


class TeamMemberActionResponse(BaseModel):
    team_id: UUID
    user_id: UUID
