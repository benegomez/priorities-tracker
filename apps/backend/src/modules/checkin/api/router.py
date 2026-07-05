from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.modules.auth.api.dependencies import CurrentUser, get_current_user
from src.modules.checkin.api.schemas import CheckInCreate, CheckInResponse, CheckInSubmitResponse
from src.modules.checkin.application.commands.create_checkin import CreateCheckInCommand, CreateCheckInUseCase
from src.modules.checkin.application.commands.submit_checkin import SubmitCheckInCommand, SubmitCheckInUseCase
from src.modules.checkin.application.queries.get_current_checkin import GetCurrentCheckInQuery, GetCurrentCheckInUseCase
from src.modules.checkin.infrastructure.repositories.checkin_repository_impl import CheckInRepositoryImpl
from src.modules.priorities.infrastructure.repositories.priority_repository_impl import PriorityRepositoryImpl
from src.shared.database.session import get_db_session
from src.shared.exceptions.base import AuthorizationException, BusinessRuleViolation, ValidationException

router = APIRouter(prefix="/checkins", tags=["checkin"])


@router.get(
    "/current",
    response_model=CheckInResponse,
    status_code=status.HTTP_200_OK,
    summary="Get current week check-in",
    description="Returns the check-in for the current week of the authenticated employee. Returns 404 if none exists.",
    operation_id="get_current_checkin",
    responses={
        401: {"description": "Not authenticated"},
        404: {"description": "No check-in for current week"},
    },
)
async def get_current_checkin(
    current_user: CurrentUser = Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session),
) -> CheckInResponse:
    use_case = GetCurrentCheckInUseCase(checkin_repo=CheckInRepositoryImpl(session))
    checkin = await use_case.execute(
        GetCurrentCheckInQuery(employee_id=current_user.user_id, organization_id=current_user.organization_id)
    )
    if checkin is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No check-in for current week")

    return CheckInResponse(
        id=checkin.id,
        employee_id=checkin.employee_id,
        organization_id=checkin.organization_id,
        week_start=checkin.week_start,
        status=checkin.status,
        submitted_at=checkin.submitted_at,
        created_at=checkin.created_at,
        updated_at=checkin.updated_at,
    )


@router.post(
    "/",
    response_model=CheckInResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a weekly check-in",
    description="Creates a new check-in for the specified week. Only one check-in per employee per week is allowed (BR-001).",
    operation_id="create_checkin",
    responses={
        401: {"description": "Not authenticated"},
        403: {"description": "Insufficient permissions"},
        409: {"description": "Check-in already exists for this week (BR-001)"},
    },
)
async def create_checkin(
    body: CheckInCreate,
    current_user: CurrentUser = Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session),
) -> CheckInResponse:
    use_case = CreateCheckInUseCase(checkin_repo=CheckInRepositoryImpl(session))
    try:
        checkin = await use_case.execute(
            CreateCheckInCommand(
                employee_id=current_user.user_id,
                organization_id=current_user.organization_id,
                week_start=body.week_start,
            )
        )
    except ValidationException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except BusinessRuleViolation as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))

    return CheckInResponse(
        id=checkin.id,
        employee_id=checkin.employee_id,
        organization_id=checkin.organization_id,
        week_start=checkin.week_start,
        status=checkin.status,
        submitted_at=checkin.submitted_at,
        created_at=checkin.created_at,
        updated_at=checkin.updated_at,
    )


@router.post(
    "/{checkin_id}/submit",
    response_model=CheckInSubmitResponse,
    status_code=status.HTTP_200_OK,
    summary="Submit a check-in",
    description="Transitions check-in from draft to submitted. Requires at least one priority. Transitions all priorities to planned.",
    operation_id="submit_checkin",
    responses={
        401: {"description": "Not authenticated"},
        403: {"description": "Cannot submit another employee's check-in"},
        404: {"description": "Check-in not found"},
        409: {"description": "Check-in has no priorities or is already submitted"},
    },
)
async def submit_checkin(
    checkin_id: UUID,
    current_user: CurrentUser = Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session),
) -> CheckInSubmitResponse:
    use_case = SubmitCheckInUseCase(
        checkin_repo=CheckInRepositoryImpl(session),
        priority_repo=PriorityRepositoryImpl(session),
    )
    try:
        checkin = await use_case.execute(
            SubmitCheckInCommand(
                checkin_id=checkin_id,
                employee_id=current_user.user_id,
                organization_id=current_user.organization_id,
            )
        )
    except AuthorizationException as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except BusinessRuleViolation as e:
        if "not found" in str(e).lower():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))

    return CheckInSubmitResponse(
        id=checkin.id,
        status=checkin.status,
        submitted_at=checkin.submitted_at,
    )
