import hashlib
from dataclasses import dataclass

from src.modules.auth.domain.repositories.user_repository import UserRepository
from src.modules.auth.domain.repositories.refresh_token_repository import RefreshTokenRepository
from src.shared.exceptions.base import AuthenticationException
from src.shared.logging.audit_logger import emit_audit_event
from src.shared.security.jwt_service import JwtService, TokenError
from src.shared.config.settings import settings


@dataclass
class RefreshCommand:
    refresh_token: str
    correlation_id: str | None = None


@dataclass
class RefreshResult:
    access_token: str
    expires_in: int


class RefreshTokenUseCase:
    def __init__(
        self,
        user_repo: UserRepository,
        refresh_token_repo: RefreshTokenRepository,
    ) -> None:
        self._user_repo = user_repo
        self._refresh_token_repo = refresh_token_repo

    async def execute(self, command: RefreshCommand) -> RefreshResult:
        # Decode to validate signature/expiry
        try:
            payload = JwtService.decode_token(command.refresh_token, refresh=True)
        except TokenError:
            raise AuthenticationException("Invalid or expired refresh token")

        # Check persisted token
        token_hash = hashlib.sha256(command.refresh_token.encode()).hexdigest()
        stored_token = await self._refresh_token_repo.get_by_hash(token_hash)

        if stored_token is None or not stored_token.is_valid():
            raise AuthenticationException("Invalid or expired refresh token")

        # Get user to include org_id and role in new access token
        user = await self._user_repo.get_by_id(stored_token.user_id)
        if user is None:
            raise AuthenticationException("Invalid or expired refresh token")

        access_token = JwtService.create_access_token(user.id, user.organization_id, user.role)

        emit_audit_event(
            "auth.token_refreshed",
            user_id=user.id,
            organization_id=user.organization_id,
            correlation_id=command.correlation_id,
        )

        return RefreshResult(
            access_token=access_token,
            expires_in=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        )
