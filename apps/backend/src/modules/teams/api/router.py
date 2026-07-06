from datetime import date, timedelta
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.modules.auth.api.dependencies import CurrentUser, require_roles
from src.modules.checkin.api.schemas import CheckInPriorityItem, CheckInResponse, CheckInTaskItem
from src.modules.crs.infrastructure.repositories.crs_repository_impl import CRSRepositoryImpl
from src.modules.teams.api.schemas import (
    CRSHistoryItem,
    TeamMemberCRS,
    TeamMemberCRSCurrent,
    TeamMemberCRSResponse,
    TeamMemberEmployee,
    TeamMemberItem,
    TeamMemberWeekStatus,
    TeamOverviewResponse,
)
from src.modules.teams.infrastructure.repositories.team_repository_impl import TeamRepositoryImpl
from src.shared.config.settings import settings
from src.shared.database.session import get_db_session

router = APIRouter(prefix="/teams", tags=["teams"])


def _get_current_week_start() -> date:
    today = date.today()
    if settings.is_development:
        return today
    return today - timedelta(days=today.weekday())


@router.get(
    "/my-team",
    response_model=TeamOverviewResponse,
    summary="Get manager's direct reports with CRS and week status",
    operation_id="get_my_team",
    responses={403: {"description": "Insufficient permissions"}},
)
async def get_my_team(
    current_user: CurrentUser = Depends(require_roles("manager", "administrator")),
    session: AsyncSession = Depends(get_db_session),
) -> TeamOverviewResponse:
    repo = TeamRepositoryImpl(session)
    week_start = _get_current_week_start()

    members = await repo.get_direct_reports(current_user.user_id, current_user.organization_id)
    if not members:
        return TeamOverviewResponse(members=[])

    member_ids = [m.id for m in members]

    crs_map = await repo.get_latest_crs_batch(member_ids, current_user.organization_id)
    checkin_map = await repo.get_week_checkins_batch(member_ids, current_user.organization_id, week_start)
    checkout_map = await repo.get_week_checkouts_batch(member_ids, current_user.organization_id, week_start)

    items = []
    for m in members:
        crs_row = crs_map.get(m.id)
        items.append(TeamMemberItem(
            id=m.id,
            first_name=m.first_name,
            last_name=m.last_name,
            email=m.email,
            crs=TeamMemberCRS(score=float(crs_row.score), trend=crs_row.trend, risk_level=crs_row.risk_level) if crs_row else None,
            week_status=TeamMemberWeekStatus(
                week_start=week_start,
                checkin_status=checkin_map.get(m.id),
                checkout_status=checkout_map.get(m.id),
            ),
        ))

    return TeamOverviewResponse(members=items)


@router.get(
    "/my-team/{employee_id}/crs",
    response_model=TeamMemberCRSResponse,
    summary="Get CRS history of a direct report",
    operation_id="get_team_member_crs",
    responses={403: {"description": "Employee is not a direct report"}},
)
async def get_team_member_crs(
    employee_id: UUID,
    weeks: int = Query(8, ge=1, le=52),
    current_user: CurrentUser = Depends(require_roles("manager", "administrator")),
    session: AsyncSession = Depends(get_db_session),
) -> TeamMemberCRSResponse:
    repo = TeamRepositoryImpl(session)
    employee = await repo.validate_direct_report(employee_id, current_user.user_id, current_user.organization_id)

    crs_repo = CRSRepositoryImpl(session)
    latest = await crs_repo.get_latest_by_employee(employee_id, current_user.organization_id)
    history_rows = await crs_repo.get_history(employee_id, current_user.organization_id, weeks)

    current = None
    if latest:
        current = TeamMemberCRSCurrent(
            score=float(latest.score), trend=latest.trend,
            risk_level=latest.risk_level, week_start=latest.week_start,
        )

    history = [CRSHistoryItem(week_start=r.week_start, score=float(r.score), trend=r.trend, risk_level=r.risk_level) for r in history_rows]

    return TeamMemberCRSResponse(
        employee=TeamMemberEmployee(id=employee.id, first_name=employee.first_name, last_name=employee.last_name),
        current=current,
        history=history,
    )


@router.get(
    "/my-team/{employee_id}/checkin",
    response_model=CheckInResponse,
    summary="Get current week check-in of a direct report (read-only)",
    operation_id="get_team_member_checkin",
    responses={
        403: {"description": "Employee is not a direct report"},
        404: {"description": "No check-in for current week"},
    },
)
async def get_team_member_checkin(
    employee_id: UUID,
    current_user: CurrentUser = Depends(require_roles("manager", "administrator")),
    session: AsyncSession = Depends(get_db_session),
) -> CheckInResponse:
    repo = TeamRepositoryImpl(session)
    await repo.validate_direct_report(employee_id, current_user.user_id, current_user.organization_id)

    week_start = _get_current_week_start()
    checkin = await repo.get_checkin_for_employee(employee_id, current_user.organization_id, week_start)
    if not checkin:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No check-in for current week")

    priorities_data = await repo.load_priorities_with_tasks(checkin.id, current_user.organization_id)
    priorities = [
        CheckInPriorityItem(
            id=p["id"], title=p["title"], description=p["description"],
            priority_level=p["priority_level"], status=p["status"],
            phase_name=p["phase_name"], project_name=p["project_name"],
            tasks=[CheckInTaskItem(id=t["id"], title=t["title"], status=t["status"]) for t in p["tasks"]],
        )
        for p in priorities_data
    ]

    return CheckInResponse(
        id=checkin.id,
        employee_id=checkin.employee_id,
        organization_id=checkin.organization_id,
        week_start=checkin.week_start,
        status=checkin.status,
        submitted_at=checkin.submitted_at,
        priorities_count=len(priorities),
        priorities=priorities,
        created_at=checkin.created_at,
        updated_at=checkin.updated_at,
    )
