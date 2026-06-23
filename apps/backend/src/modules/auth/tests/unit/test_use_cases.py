import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from uuid import uuid4
from datetime import datetime, timedelta, timezone

from src.modules.auth.application.commands.login_command import LoginCommand, LoginUseCase
from src.modules.auth.application.commands.refresh_token_command import RefreshCommand, RefreshTokenUseCase
from src.modules.auth.application.commands.logout_command import LogoutCommand, LogoutUseCase
from src.modules.auth.domain.entities.user import User
from src.modules.auth.domain.value_objects.refresh_token import RefreshToken
from src.shared.exceptions.base import AuthenticationException, AuthorizationException


def _make_user(*, active: bool = True) -> User:
    return User(
        id=uuid4(),
        organization_id=uuid4(),
        email="test@example.com",
        hashed_password="$2b$12$hashedvalue",
        role="employee",
        status="active" if active else "inactive",
        first_name="Test",
        last_name="User",
    )


def _make_refresh_token(*, valid: bool = True) -> RefreshToken:
    return RefreshToken(
        id=uuid4(),
        user_id=uuid4(),
        token_hash="somehash",
        expires_at=datetime.now(timezone.utc) + timedelta(days=7) if valid else datetime.now(timezone.utc) - timedelta(days=1),
        revoked_at=None if valid else datetime.now(timezone.utc),
    )


class TestLoginUseCase:
    @pytest.fixture
    def deps(self):
        user_repo = AsyncMock()
        refresh_token_repo = AsyncMock()
        return user_repo, refresh_token_repo

    @patch("src.modules.auth.application.commands.login_command.PasswordService")
    @patch("src.modules.auth.application.commands.login_command.JwtService")
    @patch("src.modules.auth.application.commands.login_command.emit_audit_event")
    async def test_login_valid_credentials_returns_tokens(self, mock_audit, mock_jwt, mock_pwd, deps):
        user_repo, refresh_token_repo = deps
        user = _make_user()
        user_repo.get_by_email.return_value = user
        mock_pwd.verify_password.return_value = True
        mock_jwt.create_access_token.return_value = "access_token"
        mock_jwt.create_refresh_token.return_value = "refresh_token"

        use_case = LoginUseCase(user_repo, refresh_token_repo)
        result = await use_case.execute(LoginCommand(email="test@example.com", password="pass"))

        assert result.access_token == "access_token"
        assert result.refresh_token == "refresh_token"
        assert result.expires_in > 0
        refresh_token_repo.save.assert_called_once()

    @patch("src.modules.auth.application.commands.login_command.PasswordService")
    @patch("src.modules.auth.application.commands.login_command.emit_audit_event")
    async def test_login_invalid_password_raises_authentication_exception(self, mock_audit, mock_pwd, deps):
        user_repo, refresh_token_repo = deps
        user_repo.get_by_email.return_value = _make_user()
        mock_pwd.verify_password.return_value = False

        use_case = LoginUseCase(user_repo, refresh_token_repo)
        with pytest.raises(AuthenticationException):
            await use_case.execute(LoginCommand(email="test@example.com", password="wrong"))

    @patch("src.modules.auth.application.commands.login_command.emit_audit_event")
    async def test_login_email_not_found_raises_authentication_exception(self, mock_audit, deps):
        user_repo, refresh_token_repo = deps
        user_repo.get_by_email.return_value = None

        use_case = LoginUseCase(user_repo, refresh_token_repo)
        with pytest.raises(AuthenticationException):
            await use_case.execute(LoginCommand(email="unknown@example.com", password="pass"))

    @patch("src.modules.auth.application.commands.login_command.PasswordService")
    async def test_login_inactive_user_raises_authorization_exception(self, mock_pwd, deps):
        user_repo, refresh_token_repo = deps
        user_repo.get_by_email.return_value = _make_user(active=False)
        mock_pwd.verify_password.return_value = True

        use_case = LoginUseCase(user_repo, refresh_token_repo)
        with pytest.raises(AuthorizationException):
            await use_case.execute(LoginCommand(email="test@example.com", password="pass"))

    @patch("src.modules.auth.application.commands.login_command.PasswordService")
    @patch("src.modules.auth.application.commands.login_command.JwtService")
    @patch("src.modules.auth.application.commands.login_command.emit_audit_event")
    async def test_login_success_emits_audit_event(self, mock_audit, mock_jwt, mock_pwd, deps):
        user_repo, refresh_token_repo = deps
        user = _make_user()
        user_repo.get_by_email.return_value = user
        mock_pwd.verify_password.return_value = True
        mock_jwt.create_access_token.return_value = "at"
        mock_jwt.create_refresh_token.return_value = "rt"

        use_case = LoginUseCase(user_repo, refresh_token_repo)
        await use_case.execute(LoginCommand(email="test@example.com", password="pass"))

        mock_audit.assert_called()
        call_args = mock_audit.call_args_list[-1]
        assert call_args[0][0] == "auth.login_success"

    @patch("src.modules.auth.application.commands.login_command.emit_audit_event")
    async def test_login_failure_emits_audit_event(self, mock_audit, deps):
        user_repo, refresh_token_repo = deps
        user_repo.get_by_email.return_value = None

        use_case = LoginUseCase(user_repo, refresh_token_repo)
        with pytest.raises(AuthenticationException):
            await use_case.execute(LoginCommand(email="x@x.com", password="wrong"))

        mock_audit.assert_called_once()
        assert mock_audit.call_args[0][0] == "auth.login_failed"


class TestRefreshTokenUseCase:
    @pytest.fixture
    def deps(self):
        user_repo = AsyncMock()
        refresh_token_repo = AsyncMock()
        return user_repo, refresh_token_repo

    @patch("src.modules.auth.application.commands.refresh_token_command.JwtService")
    @patch("src.modules.auth.application.commands.refresh_token_command.emit_audit_event")
    async def test_refresh_valid_token_returns_new_access_token(self, mock_audit, mock_jwt, deps):
        user_repo, refresh_token_repo = deps
        user = _make_user()
        stored_token = _make_refresh_token(valid=True)
        stored_token.user_id = user.id

        mock_jwt.decode_token.return_value = {"sub": str(user.id)}
        refresh_token_repo.get_by_hash.return_value = stored_token
        user_repo.get_by_id.return_value = user
        mock_jwt.create_access_token.return_value = "new_access_token"

        use_case = RefreshTokenUseCase(user_repo, refresh_token_repo)
        result = await use_case.execute(RefreshCommand(refresh_token="valid_refresh"))

        assert result.access_token == "new_access_token"
        assert result.expires_in > 0

    @patch("src.modules.auth.application.commands.refresh_token_command.JwtService")
    async def test_refresh_expired_token_raises_authentication_exception(self, mock_jwt, deps):
        user_repo, refresh_token_repo = deps
        stored_token = _make_refresh_token(valid=False)

        mock_jwt.decode_token.return_value = {"sub": "user-id"}
        refresh_token_repo.get_by_hash.return_value = stored_token

        use_case = RefreshTokenUseCase(user_repo, refresh_token_repo)
        with pytest.raises(AuthenticationException):
            await use_case.execute(RefreshCommand(refresh_token="expired"))

    @patch("src.modules.auth.application.commands.refresh_token_command.JwtService")
    async def test_refresh_revoked_token_raises_authentication_exception(self, mock_jwt, deps):
        user_repo, refresh_token_repo = deps
        stored_token = _make_refresh_token(valid=True)
        stored_token.revoked_at = datetime.now(timezone.utc)

        mock_jwt.decode_token.return_value = {"sub": "user-id"}
        refresh_token_repo.get_by_hash.return_value = stored_token

        use_case = RefreshTokenUseCase(user_repo, refresh_token_repo)
        with pytest.raises(AuthenticationException):
            await use_case.execute(RefreshCommand(refresh_token="revoked"))

    @patch("src.modules.auth.application.commands.refresh_token_command.JwtService")
    async def test_refresh_invalid_token_raises_authentication_exception(self, mock_jwt, deps):
        user_repo, refresh_token_repo = deps
        from src.shared.security.jwt_service import TokenError
        mock_jwt.decode_token.side_effect = TokenError("invalid")

        use_case = RefreshTokenUseCase(user_repo, refresh_token_repo)
        with pytest.raises(AuthenticationException):
            await use_case.execute(RefreshCommand(refresh_token="garbage"))


class TestLogoutUseCase:
    @patch("src.modules.auth.application.commands.logout_command.JwtService")
    @patch("src.modules.auth.application.commands.logout_command.emit_audit_event")
    async def test_logout_revokes_refresh_token(self, mock_audit, mock_jwt):
        refresh_token_repo = AsyncMock()
        mock_jwt.decode_token.return_value = {"sub": "user-id"}

        use_case = LogoutUseCase(refresh_token_repo)
        await use_case.execute(LogoutCommand(refresh_token="valid_token", user_id="uid", organization_id="oid"))

        refresh_token_repo.revoke.assert_called_once()
        mock_audit.assert_called_once()
        assert mock_audit.call_args[0][0] == "auth.logout"

    @patch("src.modules.auth.application.commands.logout_command.JwtService")
    async def test_logout_invalid_token_raises_authentication_exception(self, mock_jwt):
        refresh_token_repo = AsyncMock()
        from src.shared.security.jwt_service import TokenError
        mock_jwt.decode_token.side_effect = TokenError("invalid")

        use_case = LogoutUseCase(refresh_token_repo)
        with pytest.raises(AuthenticationException):
            await use_case.execute(LogoutCommand(refresh_token="garbage"))
