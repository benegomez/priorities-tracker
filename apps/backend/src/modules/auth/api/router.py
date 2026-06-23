import os

from fastapi import APIRouter, Depends, HTTPException, Request, status
from slowapi import Limiter
from slowapi.util import get_remote_address
from sqlalchemy.ext.asyncio import AsyncSession

from src.modules.auth.api.dependencies import CurrentUser, get_current_user
from src.modules.auth.api.schemas import (
    LoginRequest,
    LoginResponse,
    LogoutResponse,
    MeResponse,
    RefreshRequest,
    RefreshResponse,
)
from src.modules.auth.application.commands.login_command import LoginCommand, LoginUseCase
from src.modules.auth.application.commands.logout_command import LogoutCommand, LogoutUseCase
from src.modules.auth.application.commands.refresh_token_command import RefreshCommand, RefreshTokenUseCase
from src.modules.auth.infrastructure.repositories.refresh_token_repo_impl import RefreshTokenRepositoryImpl
from src.modules.auth.infrastructure.repositories.user_repo_impl import UserRepositoryImpl
from src.shared.database.session import get_db_session
from src.shared.exceptions.base import AuthenticationException, AuthorizationException

router = APIRouter(prefix="/auth", tags=["auth"])

_rate_limit_enabled = os.getenv("RATELIMIT_ENABLED", "true").lower() != "false"
_rate_limit_value = "5/minute" if _rate_limit_enabled else "9999/minute"
limiter = Limiter(key_func=get_remote_address)


@router.post(
    "/login",
    response_model=LoginResponse,
    status_code=status.HTTP_200_OK,
    summary="Authenticate user with email and password",
    description="Validates credentials and returns JWT access + refresh tokens. Rate limited to 5 req/min per IP.",
    operation_id="login",
    responses={
        400: {"description": "Invalid request body"},
        401: {"description": "Invalid credentials"},
        403: {"description": "User account inactive"},
        429: {"description": "Too many requests"},
    },
)
@limiter.limit(_rate_limit_value)
async def login(
    request: Request,
    body: LoginRequest,
    session: AsyncSession = Depends(get_db_session),
) -> LoginResponse:
    correlation_id = request.headers.get("X-Correlation-ID")
    use_case = LoginUseCase(
        user_repo=UserRepositoryImpl(session),
        refresh_token_repo=RefreshTokenRepositoryImpl(session),
    )
    try:
        result = await use_case.execute(
            LoginCommand(email=body.email, password=body.password, correlation_id=correlation_id)
        )
    except AuthenticationException:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    except AuthorizationException:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User account is inactive")

    return LoginResponse(
        access_token=result.access_token,
        refresh_token=result.refresh_token,
        expires_in=result.expires_in,
    )


@router.post(
    "/refresh",
    response_model=RefreshResponse,
    status_code=status.HTTP_200_OK,
    summary="Refresh access token",
    description="Issues a new access token using a valid refresh token. Rate limited to 5 req/min per IP.",
    operation_id="refresh_token",
    responses={
        401: {"description": "Invalid or expired refresh token"},
        429: {"description": "Too many requests"},
    },
)
@limiter.limit(_rate_limit_value)
async def refresh(
    request: Request,
    body: RefreshRequest,
    session: AsyncSession = Depends(get_db_session),
) -> RefreshResponse:
    correlation_id = request.headers.get("X-Correlation-ID")
    use_case = RefreshTokenUseCase(
        user_repo=UserRepositoryImpl(session),
        refresh_token_repo=RefreshTokenRepositoryImpl(session),
    )
    try:
        result = await use_case.execute(
            RefreshCommand(refresh_token=body.refresh_token, correlation_id=correlation_id)
        )
    except AuthenticationException:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired refresh token")

    return RefreshResponse(access_token=result.access_token, expires_in=result.expires_in)


@router.post(
    "/logout",
    response_model=LogoutResponse,
    status_code=status.HTTP_200_OK,
    summary="Logout and invalidate refresh token",
    description="Revokes the user's refresh token so it cannot be reused.",
    operation_id="logout",
    responses={401: {"description": "Not authenticated"}},
)
async def logout(
    request: Request,
    body: RefreshRequest,
    current_user: CurrentUser = Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session),
) -> LogoutResponse:
    correlation_id = request.headers.get("X-Correlation-ID")
    use_case = LogoutUseCase(refresh_token_repo=RefreshTokenRepositoryImpl(session))
    try:
        await use_case.execute(
            LogoutCommand(
                refresh_token=body.refresh_token,
                user_id=str(current_user.user_id),
                organization_id=str(current_user.organization_id),
                correlation_id=correlation_id,
            )
        )
    except AuthenticationException:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")

    return LogoutResponse(message="logged out")


@router.get(
    "/me",
    response_model=MeResponse,
    status_code=status.HTTP_200_OK,
    summary="Get current user info",
    description="Returns the authenticated user's profile from the JWT token.",
    operation_id="get_current_user_info",
    responses={401: {"description": "Not authenticated"}},
)
async def me(
    current_user: CurrentUser = Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session),
) -> MeResponse:
    user_repo = UserRepositoryImpl(session)
    user = await user_repo.get_by_id(current_user.user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

    return MeResponse(
        id=user.id,
        email=user.email,
        role=user.role,
        organization_id=user.organization_id,
        full_name=user.full_name,
    )
