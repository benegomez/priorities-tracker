import hashlib
import uuid
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone

from src.modules.auth.domain.repositories.user_repository import UserRepository
from src.modules.auth.domain.repositories.refresh_token_repository import RefreshTokenRepository
from src.modules.auth.domain.value_objects.refresh_token import RefreshToken
from src.shared.exceptions.base import AuthenticationException, AuthorizationException
from src.shared.logging.audit_logger import emit_audit_event
from src.shared.security.jwt_service import JwtService
from src.shared.security.password_service import PasswordService
from src.shared.config.settings import settings


@dataclass
class LoginCommand:
    email: str
    password: str
    correlation_id: str | None = None


@dataclass
class LoginResult:
    access_token: str
    refresh_token: str
    expires_in: int


class LoginUseCase:
    def __init__(
        self,
        user_repo: UserRepository,
        refresh_token_repo: RefreshTokenRepository,
    ) -> None:
        self._user_repo = user_repo
        self._refresh_token_repo = refresh_token_repo

    async def execute(self, command: LoginCommand) -> LoginResult:
        user = await self._user_repo.get_by_email(command.email)

        if user is None or not PasswordService.verify_password(command.password, user.hashed_password):
            emit_audit_event(
                "auth.login_failed",
                correlation_id=command.correlation_id,
                metadata={"email": command.email},
            )
            raise AuthenticationException("Invalid credentials")

        if not user.is_active():
            raise AuthorizationException("User account is inactive")

        access_token = JwtService.create_access_token(user.id, user.organization_id, user.role)
        raw_refresh_token = JwtService.create_refresh_token(user.id)

        token_hash = hashlib.sha256(raw_refresh_token.encode()).hexdigest()
        expires_at = datetime.now(timezone.utc) + timedelta(days=settings.JWT_REFRESH_TOKEN_EXPIRE_DAYS)

        refresh_token_entity = RefreshToken(
            id=uuid.uuid4(),
            user_id=user.id,
            token_hash=token_hash,
            expires_at=expires_at,
        )
        await self._refresh_token_repo.save(refresh_token_entity)

        emit_audit_event(
            "auth.login_success",
            user_id=user.id,
            organization_id=user.organization_id,
            correlation_id=command.correlation_id,
        )

        return LoginResult(
            access_token=access_token,
            refresh_token=raw_refresh_token,
            expires_in=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        )
