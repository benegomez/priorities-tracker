import pytest
from unittest.mock import AsyncMock, patch
from uuid import uuid4

from src.modules.auth.application.commands.login_command import LoginCommand, LoginUseCase
from src.modules.auth.domain.entities.user import User


def _make_user() -> User:
    return User(
        id=uuid4(),
        organization_id=uuid4(),
        email="test@example.com",
        hashed_password="$2b$12$hash",
        role="employee",
        status="active",
        first_name="Test",
        last_name="User",
    )


class TestCorrelationIdInAudit:
    @patch("src.modules.auth.application.commands.login_command.PasswordService")
    @patch("src.modules.auth.application.commands.login_command.JwtService")
    @patch("src.modules.auth.application.commands.login_command.emit_audit_event")
    async def test_correlation_id_passed_to_audit_on_success(self, mock_audit, mock_jwt, mock_pwd):
        user_repo = AsyncMock()
        refresh_token_repo = AsyncMock()
        user = _make_user()
        user_repo.get_by_email.return_value = user
        mock_pwd.verify_password.return_value = True
        mock_jwt.create_access_token.return_value = "at"
        mock_jwt.create_refresh_token.return_value = "rt"

        use_case = LoginUseCase(user_repo, refresh_token_repo)
        await use_case.execute(LoginCommand(
            email="test@example.com",
            password="pass",
            correlation_id="corr-123",
        ))

        mock_audit.assert_called()
        call_kwargs = mock_audit.call_args[1]
        assert call_kwargs["correlation_id"] == "corr-123"

    @patch("src.modules.auth.application.commands.login_command.emit_audit_event")
    async def test_correlation_id_passed_to_audit_on_failure(self, mock_audit):
        user_repo = AsyncMock()
        refresh_token_repo = AsyncMock()
        user_repo.get_by_email.return_value = None

        use_case = LoginUseCase(user_repo, refresh_token_repo)
        with pytest.raises(Exception):
            await use_case.execute(LoginCommand(
                email="x@x.com",
                password="wrong",
                correlation_id="corr-456",
            ))

        mock_audit.assert_called_once()
        call_kwargs = mock_audit.call_args[1]
        assert call_kwargs["correlation_id"] == "corr-456"
