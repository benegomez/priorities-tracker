from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.modules.auth.api.dependencies import CurrentUser, get_current_user, require_roles
from src.modules.reporting.api.schemas import (
    EmployeeInfo,
    IndividualReportResponse,
    PhaseSummary,
    ProjectInfo,
    ProjectReportResponse,
    TeamMemberSummary,
    TeamReportResponse,
    TeamWeeklyBreakdownItem,
    WeeklyBreakdownItem,
)
from src.modules.reporting.infrastructure.repositories.reporting_repository_impl import ReportingRepositoryImpl
from src.shared.database.session import get_db_session

router = APIRouter(prefix="/reports", tags=["reports"])


@router.get(
    "/individual",
    response_model=IndividualReportResponse,
    summary="Get individual commitment report",
    operation_id="get_individual_report",
)
async def get_individual_report(
    weeks: int = Query(8, ge=1, le=52),
    current_user: CurrentUser = Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session),
) -> IndividualReportResponse:
    repo = ReportingRepositoryImpl(session)

    employee = await repo.get_employee_info(current_user.user_id, current_user.organization_id)
    if not employee:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found")

    breakdown_rows = await repo.get_individual_report(current_user.user_id, current_user.organization_id, weeks)
    crs_by_week = await repo.get_crs_by_week(current_user.user_id, current_user.organization_id, weeks)
    latest_crs = await repo.get_latest_crs(current_user.user_id, current_user.organization_id)

    total = sum(r.committed for r in breakdown_rows)
    completed = sum(r.completed for r in breakdown_rows)
    carried = sum(r.carried_over for r in breakdown_rows)

    breakdown = [
        WeeklyBreakdownItem(
            week_start=r.week_start,
            committed=r.committed,
            completed=r.completed,
            carried_over=r.carried_over,
            crs=crs_by_week.get(r.week_start),
        )
        for r in breakdown_rows
    ]

    return IndividualReportResponse(
        employee=EmployeeInfo(id=str(employee.id), first_name=employee.first_name, last_name=employee.last_name),
        period_weeks=weeks,
        total_priorities=total,
        completed_priorities=completed,
        completion_rate=round(completed / total * 100, 1) if total else 0.0,
        carried_over_count=carried,
        crs_current=float(latest_crs.score) if latest_crs else None,
        crs_trend=latest_crs.trend if latest_crs else None,
        weekly_breakdown=breakdown,
    )


@router.get(
    "/team",
    response_model=TeamReportResponse,
    summary="Get team commitment report",
    operation_id="get_team_report",
    responses={403: {"description": "Insufficient permissions"}},
)
async def get_team_report(
    weeks: int = Query(8, ge=1, le=52),
    current_user: CurrentUser = Depends(require_roles("manager", "administrator")),
    session: AsyncSession = Depends(get_db_session),
) -> TeamReportResponse:
    repo = ReportingRepositoryImpl(session)

    members = await repo.get_direct_reports(current_user.user_id, current_user.organization_id)

    member_summaries = []
    crs_values = []
    for m in members:
        rate = await repo.get_member_completion_rate(m.id, current_user.organization_id, weeks)
        crs_row = await repo.get_latest_crs(m.id, current_user.organization_id)
        crs_val = float(crs_row.score) if crs_row else None
        if crs_val is not None:
            crs_values.append(crs_val)
        member_summaries.append(TeamMemberSummary(
            id=str(m.id),
            first_name=m.first_name,
            last_name=m.last_name,
            completion_rate=rate,
            crs=crs_val,
            trend=crs_row.trend if crs_row else None,
        ))

    member_ids = [m.id for m in members]
    weekly_rows = await repo.get_team_weekly_breakdown(member_ids, current_user.organization_id, weeks)

    weekly_breakdown = [
        TeamWeeklyBreakdownItem(
            week_start=r.week_start,
            checkins_submitted=r.checkins_submitted or 0,
            checkouts_submitted=r.checkouts_submitted or 0,
            avg_completion=round((r.completed_priorities / r.total_priorities * 100), 1) if r.total_priorities else 0.0,
        )
        for r in weekly_rows
    ]

    avg_rate = round(sum(m.completion_rate for m in member_summaries) / len(member_summaries), 1) if member_summaries else 0.0
    avg_crs = round(sum(crs_values) / len(crs_values), 1) if crs_values else None

    return TeamReportResponse(
        team_size=len(members),
        period_weeks=weeks,
        avg_completion_rate=avg_rate,
        avg_crs=avg_crs,
        members=member_summaries,
        weekly_breakdown=weekly_breakdown,
    )


@router.get(
    "/project/{project_id}",
    response_model=ProjectReportResponse,
    summary="Get project commitment report",
    operation_id="get_project_report",
    responses={
        403: {"description": "Insufficient permissions"},
        404: {"description": "Project not found"},
    },
)
async def get_project_report(
    project_id: UUID,
    weeks: int = Query(8, ge=1, le=52),
    current_user: CurrentUser = Depends(require_roles("manager", "administrator")),
    session: AsyncSession = Depends(get_db_session),
) -> ProjectReportResponse:
    repo = ReportingRepositoryImpl(session)

    project = await repo.get_project(project_id, current_user.organization_id)
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")

    phase_rows = await repo.get_project_phases_report(project_id, current_user.organization_id, weeks)

    phases = [
        PhaseSummary(
            id=str(r.id),
            name=r.name,
            total_priorities=r.total_priorities or 0,
            completed_priorities=r.completed_priorities or 0,
            completion_rate=round((r.completed_priorities / r.total_priorities * 100), 1) if r.total_priorities else 0.0,
        )
        for r in phase_rows
    ]

    total = sum(p.total_priorities for p in phases)
    completed = sum(p.completed_priorities for p in phases)

    return ProjectReportResponse(
        project=ProjectInfo(id=str(project.id), name=project.name, status=project.status),
        period_weeks=weeks,
        total_priorities=total,
        completed_priorities=completed,
        completion_rate=round(completed / total * 100, 1) if total else 0.0,
        phases=phases,
    )
