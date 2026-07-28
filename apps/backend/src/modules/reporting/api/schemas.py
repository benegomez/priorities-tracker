from datetime import date
from pydantic import BaseModel


class EmployeeInfo(BaseModel):
    id: str
    first_name: str
    last_name: str


class WeeklyBreakdownItem(BaseModel):
    week_start: date
    committed: int
    completed: int
    carried_over: int
    crs: float | None


class IndividualReportResponse(BaseModel):
    employee: EmployeeInfo
    period_weeks: int
    total_priorities: int
    completed_priorities: int
    completion_rate: float
    carried_over_count: int
    crs_current: float | None
    crs_trend: str | None
    weekly_breakdown: list[WeeklyBreakdownItem]


class TeamMemberSummary(BaseModel):
    id: str
    first_name: str
    last_name: str
    completion_rate: float
    crs: float | None
    trend: str | None


class TeamWeeklyBreakdownItem(BaseModel):
    week_start: date
    checkins_submitted: int
    checkouts_submitted: int
    avg_completion: float


class TeamReportResponse(BaseModel):
    team_size: int
    period_weeks: int
    avg_completion_rate: float
    avg_crs: float | None
    members: list[TeamMemberSummary]
    weekly_breakdown: list[TeamWeeklyBreakdownItem]


class ProjectInfo(BaseModel):
    id: str
    name: str
    status: str


class PhaseSummary(BaseModel):
    id: str
    name: str
    total_priorities: int
    completed_priorities: int
    completion_rate: float


class ProjectReportResponse(BaseModel):
    project: ProjectInfo
    period_weeks: int
    total_priorities: int
    completed_priorities: int
    completion_rate: float
    phases: list[PhaseSummary]
