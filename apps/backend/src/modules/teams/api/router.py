import math
from datetime import date, timedelta
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.modules.auth.api.dependencies import CurrentUser, require_roles
from src.modules.checkin.api.schemas import CheckInPriorityItem, CheckInResponse, CheckInTaskItem
from src.modules.crs.infrastructure.repositories.crs_repository_impl import CRSRepositoryImpl
from src.modules.teams.api.schemas import (
    AdminTeamDetailResponse,
    AdminTeamListResponse,
    AdminTeamMemberItem,
    AdminTeamResponse,
    CRSHistoryItem,
    TeamCreate,
    TeamMemberActionResponse,
    TeamMemberAdd,
    TeamMemberCRS,
    TeamMemberCRSCurrent,
    TeamMemberCRSResponse,
    TeamMemberEmployee,
    TeamMemberItem,
    TeamMemberWeekStatus,
    TeamOverviewResponse,
    TeamUpdate,
)
from src.modules.teams.application.commands.create_update_team import (
    CreateTeamCommand,
    CreateTeamUseCase,
    UpdateTeamCommand,
    UpdateTeamUseCase,
)
from src.modules.teams.application.commands.manage_members import (
    AddMemberCommand,
    AddMemberUseCase,
    RemoveMemberCommand,
    RemoveMemberUseCase,
)
from src.modules.teams.infrastructure.repositories.team_admin_repo_impl import TeamAdminRepoImpl
from src.modules.teams.infrastructure.repositories.team_repository_impl import TeamRepositoryImpl
from src.shared.config.settings import settings
from src.shared.database.session import get_db_session
from src.shared.exceptions.base import BusinessRuleViolation

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


# ── Admin Team Management endpoints ─────────────────────────────────────────────


def _admin_repo(session: AsyncSession) -> TeamAdminRepoImpl:
    return TeamAdminRepoImpl(session)


@router.get(
    "",
    response_model=AdminTeamListResponse,
    summary="List teams in the organization",
    operation_id="list_teams",
    responses={403: {"description": "Insufficient permissions"}},
)
async def list_teams(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    current_user: CurrentUser = Depends(require_roles("administrator")),
    session: AsyncSession = Depends(get_db_session),
) -> AdminTeamListResponse:
    repo = _admin_repo(session)
    items, total = await repo.list_teams(current_user.organization_id, page, page_size)
    return AdminTeamListResponse(
        items=[_to_admin_response(t) for t in items],
        total=total,
        page=page,
        page_size=page_size,
        pages=math.ceil(total / page_size) if total else 0,
    )


@router.post(
    "",
    response_model=AdminTeamResponse,
    status_code=201,
    summary="Create a new team",
    operation_id="create_team",
    responses={
        409: {"description": "Team name already exists"},
        404: {"description": "Manager not found"},
        403: {"description": "Insufficient permissions"},
    },
)
async def create_team(
    body: TeamCreate,
    current_user: CurrentUser = Depends(require_roles("administrator")),
    session: AsyncSession = Depends(get_db_session),
) -> AdminTeamResponse:
    use_case = CreateTeamUseCase(_admin_repo(session))
    try:
        team = await use_case.execute(CreateTeamCommand(
            organization_id=current_user.organization_id,
            name=body.name,
            manager_id=body.manager_id,
        ))
        await session.commit()
    except BusinessRuleViolation as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    return _to_admin_response(team)


@router.get(
    "/{team_id}",
    response_model=AdminTeamDetailResponse,
    summary="Get team detail with members",
    operation_id="get_team",
    responses={
        404: {"description": "Team not found"},
        403: {"description": "Insufficient permissions"},
    },
)
async def get_team(
    team_id: UUID,
    current_user: CurrentUser = Depends(require_roles("administrator")),
    session: AsyncSession = Depends(get_db_session),
) -> AdminTeamDetailResponse:
    repo = _admin_repo(session)
    team = await repo.get_by_id(team_id, current_user.organization_id)
    if not team:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Team not found")
    members = await repo.get_members(team_id, current_user.organization_id)
    response = AdminTeamDetailResponse(**_to_admin_response(team).__dict__)
    response.members = [
        AdminTeamMemberItem(id=m.id, first_name=m.first_name, last_name=m.last_name, role=m.role, status=m.status)
        for m in members
    ]
    return response


@router.patch(
    "/{team_id}",
    response_model=AdminTeamResponse,
    summary="Update team name or manager",
    operation_id="update_team",
    responses={
        409: {"description": "Team name already exists"},
        404: {"description": "Team not found"},
        403: {"description": "Insufficient permissions"},
    },
)
async def update_team(
    team_id: UUID,
    body: TeamUpdate,
    current_user: CurrentUser = Depends(require_roles("administrator")),
    session: AsyncSession = Depends(get_db_session),
) -> AdminTeamResponse:
    use_case = UpdateTeamUseCase(_admin_repo(session))
    try:
        team = await use_case.execute(UpdateTeamCommand(
            team_id=team_id,
            organization_id=current_user.organization_id,
            name=body.name,
            manager_id=body.manager_id,
        ))
        await session.commit()
    except BusinessRuleViolation as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except ValueError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Team not found")
    return _to_admin_response(team)


@router.post(
    "/{team_id}/members",
    response_model=TeamMemberActionResponse,
    summary="Assign a user to a team",
    operation_id="add_team_member",
    responses={
        409: {"description": "User is already a member of this team"},
        404: {"description": "Team or user not found"},
        403: {"description": "Insufficient permissions"},
    },
)
async def add_team_member(
    team_id: UUID,
    body: TeamMemberAdd,
    current_user: CurrentUser = Depends(require_roles("administrator")),
    session: AsyncSession = Depends(get_db_session),
) -> TeamMemberActionResponse:
    use_case = AddMemberUseCase(_admin_repo(session))
    try:
        await use_case.execute(AddMemberCommand(
            team_id=team_id,
            user_id=body.user_id,
            organization_id=current_user.organization_id,
        ))
        await session.commit()
    except BusinessRuleViolation as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    return TeamMemberActionResponse(team_id=team_id, user_id=body.user_id)


@router.delete(
    "/{team_id}/members/{user_id}",
    status_code=204,
    summary="Remove a user from a team",
    operation_id="remove_team_member",
    responses={
        404: {"description": "User is not a member of this team"},
        403: {"description": "Insufficient permissions"},
    },
)
async def remove_team_member(
    team_id: UUID,
    user_id: UUID,
    current_user: CurrentUser = Depends(require_roles("administrator")),
    session: AsyncSession = Depends(get_db_session),
) -> None:
    use_case = RemoveMemberUseCase(_admin_repo(session))
    try:
        await use_case.execute(RemoveMemberCommand(
            team_id=team_id,
            user_id=user_id,
            organization_id=current_user.organization_id,
        ))
        await session.commit()
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


def _to_admin_response(team) -> AdminTeamResponse:
    return AdminTeamResponse(
        id=team.id,
        name=team.name,
        manager_id=team.manager_id,
        manager_name=team.manager_name,
        member_count=team.member_count,
        created_at=team.created_at,
        updated_at=team.updated_at,
    )
