from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from src.modules.auth.api.dependencies import CurrentUser, get_current_user
from src.modules.checkout.api.schemas import (
    CheckOutCreate, CheckOutResponse, CheckOutPriorityItem, CheckOutTaskItem,
    CheckOutSubmitRequest, CheckOutSubmitResponse, CheckOutSummaryResponse,
    MarkCompletedRequest, MarkPriorityResponse, MarkTaskResponse,
)
from src.modules.checkout.application.commands.create_checkout import CreateCheckOutCommand, CreateCheckOutUseCase
from src.modules.checkout.application.commands.mark_priority import MarkPriorityCommand, MarkPriorityCompletedUseCase
from src.modules.checkout.application.commands.mark_task import MarkTaskCommand, MarkTaskCompletedUseCase
from src.modules.checkout.application.commands.submit_checkout import SubmitCheckOutCommand, SubmitCheckOutUseCase
from src.modules.checkout.application.queries.get_current_checkout import GetCurrentCheckOutQuery, GetCurrentCheckOutUseCase
from src.modules.checkout.infrastructure.repositories.checkout_repository_impl import CheckOutRepositoryImpl
from src.shared.database.session import get_db_session
from src.shared.exceptions.base import AuthorizationException, BusinessRuleViolation

router = APIRouter(prefix="/checkouts", tags=["checkout"])


async def _load_priorities_for_checkout(session: AsyncSession, checkin_id: UUID, checkout_id: UUID, organization_id: UUID) -> list[CheckOutPriorityItem]:
    # Load priorities
    result = await session.execute(
        text("""
            SELECT id, title, status, priority_level, completed_in_checkout
            FROM priorities
            WHERE checkin_id = :checkin_id AND organization_id = :organization_id AND deleted_at IS NULL
            ORDER BY created_at
        """),
        {"checkin_id": checkin_id, "organization_id": organization_id},
    )
    priorities = result.fetchall()

    # Load tasks for all priorities in one query
    priority_ids = [p.id for p in priorities]
    tasks_by_priority: dict[UUID, list[CheckOutTaskItem]] = {pid: [] for pid in priority_ids}

    if priority_ids:
        task_result = await session.execute(
            text("""
                SELECT id, priority_id, title, status, completed_in_checkout
                FROM tasks
                WHERE priority_id = ANY(:priority_ids) AND organization_id = :organization_id AND deleted_at IS NULL
                ORDER BY created_at
            """),
            {"priority_ids": priority_ids, "organization_id": organization_id},
        )
        for t in task_result.fetchall():
            tasks_by_priority[t.priority_id].append(
                CheckOutTaskItem(id=t.id, title=t.title, status=t.status, completed=t.completed_in_checkout == checkout_id)
            )

    return [
        CheckOutPriorityItem(
            id=row.id, title=row.title, status=row.status, priority_level=row.priority_level,
            completed=row.completed_in_checkout == checkout_id,
            tasks=tasks_by_priority.get(row.id, []),
        )
        for row in priorities
    ]


@router.get(
    "/current",
    response_model=CheckOutResponse,
    summary="Get current week check-out",
    operation_id="get_current_checkout",
    responses={404: {"description": "No check-out for current week"}},
)
async def get_current_checkout(
    current_user: CurrentUser = Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session),
) -> CheckOutResponse:
    use_case = GetCurrentCheckOutUseCase(checkout_repo=CheckOutRepositoryImpl(session))
    checkout = await use_case.execute(
        GetCurrentCheckOutQuery(employee_id=current_user.user_id, organization_id=current_user.organization_id)
    )
    if checkout is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No check-out for current week")

    priorities = await _load_priorities_for_checkout(session, checkout.checkin_id, checkout.id, current_user.organization_id)

    return CheckOutResponse(
        id=checkout.id, checkin_id=checkout.checkin_id, employee_id=checkout.employee_id,
        organization_id=checkout.organization_id, week_start=checkout.week_start,
        status=checkout.status, submitted_at=checkout.submitted_at,
        notes=checkout.notes, lessons_learned=checkout.lessons_learned,
        priorities=priorities, created_at=checkout.created_at, updated_at=checkout.updated_at,
    )


@router.post(
    "/",
    response_model=CheckOutResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a weekly check-out",
    operation_id="create_checkout",
    responses={409: {"description": "BR-002 or check-in not submitted"}},
)
async def create_checkout(
    body: CheckOutCreate,
    current_user: CurrentUser = Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session),
) -> CheckOutResponse:
    use_case = CreateCheckOutUseCase(checkout_repo=CheckOutRepositoryImpl(session), session=session)
    try:
        checkout = await use_case.execute(
            CreateCheckOutCommand(checkin_id=body.checkin_id, employee_id=current_user.user_id, organization_id=current_user.organization_id)
        )
    except AuthorizationException as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except BusinessRuleViolation as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))

    priorities = await _load_priorities_for_checkout(session, checkout.checkin_id, checkout.id, current_user.organization_id)

    return CheckOutResponse(
        id=checkout.id, checkin_id=checkout.checkin_id, employee_id=checkout.employee_id,
        organization_id=checkout.organization_id, week_start=checkout.week_start,
        status=checkout.status, submitted_at=checkout.submitted_at,
        priorities=priorities, created_at=checkout.created_at, updated_at=checkout.updated_at,
    )


@router.patch(
    "/{checkout_id}/priorities/{priority_id}",
    response_model=MarkPriorityResponse,
    summary="Mark priority as completed/uncompleted",
    operation_id="mark_priority_completed",
    responses={409: {"description": "Check-out already submitted"}},
)
async def mark_priority(
    checkout_id: UUID,
    priority_id: UUID,
    body: MarkCompletedRequest,
    current_user: CurrentUser = Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session),
) -> MarkPriorityResponse:
    use_case = MarkPriorityCompletedUseCase(checkout_repo=CheckOutRepositoryImpl(session), session=session)
    try:
        await use_case.execute(
            MarkPriorityCommand(checkout_id=checkout_id, priority_id=priority_id, completed=body.completed, employee_id=current_user.user_id, organization_id=current_user.organization_id)
        )
    except AuthorizationException as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except BusinessRuleViolation as e:
        if "not found" in str(e).lower():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))

    return MarkPriorityResponse(priority_id=priority_id, completed=body.completed)


@router.patch(
    "/{checkout_id}/tasks/{task_id}",
    response_model=MarkTaskResponse,
    summary="Mark task as completed/uncompleted",
    operation_id="mark_task_completed",
    responses={409: {"description": "Check-out already submitted"}},
)
async def mark_task(
    checkout_id: UUID,
    task_id: UUID,
    body: MarkCompletedRequest,
    current_user: CurrentUser = Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session),
) -> MarkTaskResponse:
    use_case = MarkTaskCompletedUseCase(checkout_repo=CheckOutRepositoryImpl(session), session=session)
    try:
        await use_case.execute(
            MarkTaskCommand(checkout_id=checkout_id, task_id=task_id, completed=body.completed, employee_id=current_user.user_id, organization_id=current_user.organization_id)
        )
    except AuthorizationException as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except BusinessRuleViolation as e:
        if "not found" in str(e).lower():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))

    return MarkTaskResponse(task_id=task_id, completed=body.completed)


@router.post(
    "/{checkout_id}/submit",
    response_model=CheckOutSubmitResponse,
    summary="Submit check-out",
    operation_id="submit_checkout",
    responses={409: {"description": "Already submitted"}},
)
async def submit_checkout(
    checkout_id: UUID,
    body: CheckOutSubmitRequest,
    current_user: CurrentUser = Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session),
) -> CheckOutSubmitResponse:
    use_case = SubmitCheckOutUseCase(checkout_repo=CheckOutRepositoryImpl(session), session=session)
    try:
        checkout, summary = await use_case.execute(
            SubmitCheckOutCommand(
                checkout_id=checkout_id, employee_id=current_user.user_id,
                organization_id=current_user.organization_id,
                notes=body.notes, lessons_learned=body.lessons_learned,
            )
        )
    except AuthorizationException as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except BusinessRuleViolation as e:
        if "not found" in str(e).lower():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))

    return CheckOutSubmitResponse(
        id=checkout.id, status=checkout.status, submitted_at=checkout.submitted_at,
        summary=CheckOutSummaryResponse(
            priorities_total=summary.priorities_total,
            priorities_completed=summary.priorities_completed,
            priorities_carried=summary.priorities_carried,
            tasks_total=summary.tasks_total,
            tasks_completed=summary.tasks_completed,
        ),
    )
