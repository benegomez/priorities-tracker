import math
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.modules.auth.api.dependencies import CurrentUser, require_roles
from src.modules.users.api.schemas import (
    UserCreate,
    UserCreatedResponse,
    UserListResponse,
    UserResponse,
    UserStatusResponse,
    UserStatusUpdate,
    UserUpdate,
)
from src.modules.users.application.commands.create_user import CreateUserCommand, CreateUserUseCase
from src.modules.users.application.commands.update_user import (
    UpdateUserCommand,
    UpdateUserStatusCommand,
    UpdateUserStatusUseCase,
    UpdateUserUseCase,
)
from src.modules.users.application.queries.get_users import GetUserByIdUseCase, GetUsersQuery, GetUsersUseCase
from src.modules.users.infrastructure.repositories.user_management_repo_impl import UserManagementRepoImpl
from src.shared.database.session import get_db_session
from src.shared.exceptions.base import BusinessRuleViolation

router = APIRouter(prefix="/users", tags=["users"])


def _repo(session: AsyncSession) -> UserManagementRepoImpl:
    return UserManagementRepoImpl(session)


@router.get(
    "",
    response_model=UserListResponse,
    summary="List users in the organization",
    operation_id="list_users",
    responses={403: {"description": "Insufficient permissions"}},
)
async def list_users(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    role: str | None = Query(None),
    status: str | None = Query(None),
    current_user: CurrentUser = Depends(require_roles("administrator")),
    session: AsyncSession = Depends(get_db_session),
) -> UserListResponse:
    use_case = GetUsersUseCase(_repo(session))
    result = await use_case.execute(GetUsersQuery(
        organization_id=current_user.organization_id,
        role=role,
        status=status,
        page=page,
        page_size=page_size,
    ))
    return UserListResponse(
        items=[_to_response(u) for u in result.items],
        total=result.total,
        page=result.page,
        page_size=result.page_size,
        pages=math.ceil(result.total / result.page_size) if result.total else 0,
    )


@router.post(
    "",
    response_model=UserCreatedResponse,
    status_code=201,
    summary="Create a new user",
    operation_id="create_user",
    responses={
        409: {"description": "Email already exists in organization"},
        404: {"description": "Manager not found"},
        403: {"description": "Insufficient permissions"},
    },
)
async def create_user(
    body: UserCreate,
    current_user: CurrentUser = Depends(require_roles("administrator")),
    session: AsyncSession = Depends(get_db_session),
) -> UserCreatedResponse:
    use_case = CreateUserUseCase(_repo(session))
    try:
        result = await use_case.execute(CreateUserCommand(
            organization_id=current_user.organization_id,
            email=body.email,
            first_name=body.first_name,
            last_name=body.last_name,
            role=body.role,
            manager_id=body.manager_id,
        ))
        await session.commit()
    except BusinessRuleViolation as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

    return UserCreatedResponse(**_to_response(result.user).__dict__, temporary_password=result.temporary_password)


@router.get(
    "/{user_id}",
    response_model=UserResponse,
    summary="Get user detail",
    operation_id="get_user",
    responses={
        404: {"description": "User not found"},
        403: {"description": "Insufficient permissions"},
    },
)
async def get_user(
    user_id: UUID,
    current_user: CurrentUser = Depends(require_roles("administrator")),
    session: AsyncSession = Depends(get_db_session),
) -> UserResponse:
    use_case = GetUserByIdUseCase(_repo(session))
    try:
        user = await use_case.execute(user_id, current_user.organization_id)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return _to_response(user)


@router.patch(
    "/{user_id}",
    response_model=UserResponse,
    summary="Update user data",
    operation_id="update_user",
    responses={
        409: {"description": "Cannot change own role"},
        404: {"description": "User not found"},
        403: {"description": "Insufficient permissions"},
    },
)
async def update_user(
    user_id: UUID,
    body: UserUpdate,
    current_user: CurrentUser = Depends(require_roles("administrator")),
    session: AsyncSession = Depends(get_db_session),
) -> UserResponse:
    use_case = UpdateUserUseCase(_repo(session))
    try:
        user = await use_case.execute(UpdateUserCommand(
            user_id=user_id,
            organization_id=current_user.organization_id,
            requesting_user_id=current_user.user_id,
            first_name=body.first_name,
            last_name=body.last_name,
            role=body.role,
            manager_id=body.manager_id,
        ))
        await session.commit()
    except BusinessRuleViolation as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except ValueError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return _to_response(user)


@router.patch(
    "/{user_id}/status",
    response_model=UserStatusResponse,
    summary="Activate or deactivate a user",
    operation_id="update_user_status",
    responses={
        409: {"description": "Cannot deactivate own account"},
        404: {"description": "User not found"},
        403: {"description": "Insufficient permissions"},
    },
)
async def update_user_status(
    user_id: UUID,
    body: UserStatusUpdate,
    current_user: CurrentUser = Depends(require_roles("administrator")),
    session: AsyncSession = Depends(get_db_session),
) -> UserStatusResponse:
    use_case = UpdateUserStatusUseCase(_repo(session))
    try:
        user = await use_case.execute(UpdateUserStatusCommand(
            user_id=user_id,
            organization_id=current_user.organization_id,
            requesting_user_id=current_user.user_id,
            status=body.status,
        ))
        await session.commit()
    except BusinessRuleViolation as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except ValueError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return UserStatusResponse(id=user.id, status=user.status)


def _to_response(user) -> UserResponse:
    return UserResponse(
        id=user.id,
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        role=user.role,
        status=user.status,
        manager_id=user.manager_id,
        manager_name=user.manager_name,
    )
