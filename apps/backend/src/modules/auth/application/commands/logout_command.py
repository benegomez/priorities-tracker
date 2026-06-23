import hashlib
from dataclasses import dataclass

from src.modules.auth.domain.repositories.refresh_token_repository import RefreshTokenRepository
from src.shared.logging.audit_logger import emit_audit_event
from src.shared.security.jwt_service import JwtService, TokenError
from src.shared.exceptions.base import AuthenticationException


@dataclass
class LogoutCommand:
    refresh_token: str
    user_id: str | None = None
    organization_id: str | None = None
    correlation_id: str | None = None


class LogoutUseCase:
    def __init__(self, refresh_token_repo: RefreshTokenRepository) -> None:
        self._refresh_token_repo = refresh_token_repo

    async def execute(self, command: LogoutCommand) -> None:
        try:
            JwtService.decode_token(command.refresh_token, refresh=True)
        except TokenError:
            raise AuthenticationException("Invalid refresh token")

        token_hash = hashlib.sha256(command.refresh_token.encode()).hexdigest()
        await self._refresh_token_repo.revoke(token_hash)

        emit_audit_event(
            "auth.logout",
            user_id=command.user_id,
            organization_id=command.organization_id,
            correlation_id=command.correlation_id,
        )
