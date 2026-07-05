from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.modules.auth.api.dependencies import CurrentUser, get_current_user
from src.modules.checkin.infrastructure.repositories.checkin_repository_impl import CheckInRepositoryImpl
from src.modules.priorities.api.schemas import PriorityCreate, PriorityResponse, TaskCreate, TaskResponse
from src.modules.priorities.application.commands.create_priority import CreatePriorityCommand, CreatePriorityUseCase
from src.modules.priorities.application.commands.create_task import CreateTaskCommand, CreateTaskUseCase
from src.modules.priorities.infrastructure.repositories.priority_repository_impl import PriorityRepositoryImpl
from src.modules.priorities.infrastructure.repositories.task_repository_impl import TaskRepositoryImpl
from src.shared.database.session import get_db_session
from src.shared.exceptions.base import AuthorizationException, BusinessRuleViolation, ValidationException

router = APIRouter(prefix="/priorities", tags=["priorities"])


@router.post(
    "/",
    response_model=PriorityResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a priority",
    description="Adds a priority to a check-in. Phase must belong to an active project in the same organization (BR-003, BR-004).",
    operation_id="create_priority",
    responses={
        401: {"description": "Not authenticated"},
        403: {"description": "Cross-tenant access or not owner of check-in"},
        404: {"description": "Check-in or phase not found"},
        409: {"description": "Check-in already submitted"},
    },
)
async def create_priority(
    body: PriorityCreate,
    current_user: CurrentUser = Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session),
) -> PriorityResponse:
    use_case = CreatePriorityUseCase(
        priority_repo=PriorityRepositoryImpl(session),
        checkin_repo=CheckInRepositoryImpl(session),
        session=session,
    )
    try:
        priority = await use_case.execute(
            CreatePriorityCommand(
                checkin_id=body.checkin_id,
                phase_id=body.phase_id,
                title=body.title,
                description=body.description,
                priority_level=body.priority_level,
                employee_id=current_user.user_id,
                organization_id=current_user.organization_id,
            )
        )
    except ValidationException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except AuthorizationException as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except BusinessRuleViolation as e:
        if "not found" in str(e).lower():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))

    return PriorityResponse(
        id=priority.id,
        checkin_id=priority.checkin_id,
        phase_id=priority.phase_id,
        owner_id=priority.owner_id,
        organization_id=priority.organization_id,
        title=priority.title,
        description=priority.description,
        priority_level=priority.priority_level,
        status=priority.status,
        week_start=priority.week_start,
        created_at=priority.created_at,
        updated_at=priority.updated_at,
    )


@router.post(
    "/{priority_id}/tasks",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a task",
    description="Adds a task to a priority. Priority must belong to the authenticated employee (BR-005, BR-013).",
    operation_id="create_task",
    responses={
        401: {"description": "Not authenticated"},
        403: {"description": "Priority does not belong to employee"},
        404: {"description": "Priority not found"},
    },
)
async def create_task(
    priority_id: UUID,
    body: TaskCreate,
    current_user: CurrentUser = Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session),
) -> TaskResponse:
    use_case = CreateTaskUseCase(
        task_repo=TaskRepositoryImpl(session),
        priority_repo=PriorityRepositoryImpl(session),
    )
    try:
        task = await use_case.execute(
            CreateTaskCommand(
                priority_id=priority_id,
                title=body.title,
                description=body.description,
                employee_id=current_user.user_id,
                organization_id=current_user.organization_id,
            )
        )
    except ValidationException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except AuthorizationException as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except BusinessRuleViolation as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

    return TaskResponse(
        id=task.id,
        priority_id=task.priority_id,
        organization_id=task.organization_id,
        title=task.title,
        description=task.description,
        status=task.status,
        created_at=task.created_at,
        updated_at=task.updated_at,
    )
