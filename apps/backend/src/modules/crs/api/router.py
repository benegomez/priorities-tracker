from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.modules.auth.api.dependencies import CurrentUser, get_current_user
from src.modules.crs.api.schemas import CRSCurrentResponse, CRSHistoryItem, CRSHistoryResponse
from src.modules.crs.infrastructure.repositories.crs_repository_impl import CRSRepositoryImpl
from src.shared.database.session import get_db_session

router = APIRouter(prefix="/crs", tags=["crs"])


@router.get("/current", response_model=CRSCurrentResponse, summary="Get current CRS score")
async def get_current_crs(
    current_user: CurrentUser = Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session),
) -> CRSCurrentResponse:
    repo = CRSRepositoryImpl(session)
    row = await repo.get_latest_by_employee(current_user.user_id, current_user.organization_id)
    if row is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No CRS calculated yet")

    return CRSCurrentResponse(
        score=float(row.score),
        trend=row.trend,
        risk_level=row.risk_level,
        week_start=row.week_start,
        formula_version=row.formula_version,
        priorities_total=row.priorities_total,
        priorities_completed=row.priorities_completed,
        tasks_total=row.tasks_total,
        tasks_completed=row.tasks_completed,
    )


@router.get("/history", response_model=CRSHistoryResponse, summary="Get CRS history")
async def get_crs_history(
    weeks: int = Query(8, ge=1, le=52),
    current_user: CurrentUser = Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session),
) -> CRSHistoryResponse:
    repo = CRSRepositoryImpl(session)
    rows = await repo.get_history(current_user.user_id, current_user.organization_id, weeks)
    items = [CRSHistoryItem(week_start=r.week_start, score=float(r.score), trend=r.trend, risk_level=r.risk_level) for r in rows]
    return CRSHistoryResponse(items=items)
