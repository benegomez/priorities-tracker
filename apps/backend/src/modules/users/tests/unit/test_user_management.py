"""Unit tests for US-012 Admin User Management use cases."""
import string
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pytest

from src.modules.users.application.commands.create_user import (
    CreateUserCommand,
    CreateUserUseCase,
    generate_temporary_password,
)
from src.modules.users.application.commands.update_user import (
    UpdateUserCommand,
    UpdateUserStatusCommand,
    UpdateUserStatusUseCase,
    UpdateUserUseCase,
)
from src.modules.users.domain.entities.user_detail import UserDetail
from src.shared.exceptions.base import BusinessRuleViolation


def _make_user(**kwargs) -> UserDetail:
    defaults = dict(
        id=uuid4(),
        organization_id=uuid4(),
        manager_id=None,
        email="user@test.com",
        role="employee",
        status="active",
        first_name="Test",
        last_name="User",
        manager_name=None,
    )
    defaults.update(kwargs)
    return UserDetail(**defaults)


# ── generate_temporary_password ───────────────────────────────────────────────

class TestGenerateTemporaryPassword:
    def test_length_is_at_least_12(self):
        pwd = generate_temporary_password()
        assert len(pwd) >= 12

    def test_contains_uppercase(self):
        pwd = generate_temporary_password()
        assert any(c in string.ascii_uppercase for c in pwd)

    def test_contains_digit(self):
        pwd = generate_temporary_password()
        assert any(c in string.digits for c in pwd)

    def test_contains_special(self):
        pwd = generate_temporary_password()
        assert any(c in "!@#$" for c in pwd)


# ── CreateUserUseCase ─────────────────────────────────────────────────────────

class TestCreateUserUseCase:
    @pytest.fixture
    def repo(self):
        r = AsyncMock()
        r.email_exists.return_value = False
        r.manager_exists.return_value = True
        return r

    async def test_create_user_returns_user_with_temporary_password(self, repo):
        org_id = uuid4()
        user = _make_user(organization_id=org_id)
        repo.create.return_value = user

        result = await CreateUserUseCase(repo).execute(CreateUserCommand(
            organization_id=org_id,
            email="new@test.com",
            first_name="Ana",
            last_name="García",
            role="employee",
            manager_id=None,
        ))

        assert result.user == user
        assert len(result.temporary_password) >= 12
        repo.create.assert_called_once()

    async def test_create_user_raises_409_on_duplicate_email(self, repo):
        repo.email_exists.return_value = True

        with pytest.raises(BusinessRuleViolation, match="BR-NEW-04"):
            await CreateUserUseCase(repo).execute(CreateUserCommand(
                organization_id=uuid4(),
                email="dup@test.com",
                first_name="X",
                last_name="Y",
                role="employee",
                manager_id=None,
            ))

    async def test_create_user_raises_404_on_invalid_manager(self, repo):
        repo.manager_exists.return_value = False

        with pytest.raises(ValueError, match="not found"):
            await CreateUserUseCase(repo).execute(CreateUserCommand(
                organization_id=uuid4(),
                email="new@test.com",
                first_name="X",
                last_name="Y",
                role="employee",
                manager_id=uuid4(),
            ))


# ── UpdateUserUseCase ─────────────────────────────────────────────────────────

class TestUpdateUserUseCase:
    async def test_update_user_raises_409_on_self_role_change(self):
        repo = AsyncMock()
        user_id = uuid4()

        with pytest.raises(BusinessRuleViolation, match="BR-NEW-02"):
            await UpdateUserUseCase(repo).execute(UpdateUserCommand(
                user_id=user_id,
                organization_id=uuid4(),
                requesting_user_id=user_id,  # same user
                first_name=None,
                last_name=None,
                role="employee",  # trying to change own role
                manager_id=None,
            ))

    async def test_update_user_succeeds_when_not_self_role_change(self):
        repo = AsyncMock()
        user = _make_user()
        repo.update.return_value = user

        result = await UpdateUserUseCase(repo).execute(UpdateUserCommand(
            user_id=uuid4(),
            organization_id=uuid4(),
            requesting_user_id=uuid4(),  # different user
            first_name="Nuevo",
            last_name=None,
            role="manager",
            manager_id=None,
        ))
        assert result == user


# ── UpdateUserStatusUseCase ───────────────────────────────────────────────────

class TestUpdateUserStatusUseCase:
    async def test_deactivate_user_raises_409_on_self_deactivation(self):
        repo = AsyncMock()
        user_id = uuid4()

        with pytest.raises(BusinessRuleViolation, match="BR-NEW-01"):
            await UpdateUserStatusUseCase(repo).execute(UpdateUserStatusCommand(
                user_id=user_id,
                organization_id=uuid4(),
                requesting_user_id=user_id,  # same user
                status="inactive",
            ))

    async def test_deactivate_other_user_succeeds(self):
        repo = AsyncMock()
        user = _make_user(status="inactive")
        repo.update_status.return_value = user

        result = await UpdateUserStatusUseCase(repo).execute(UpdateUserStatusCommand(
            user_id=uuid4(),
            organization_id=uuid4(),
            requesting_user_id=uuid4(),  # different user
            status="inactive",
        ))
        assert result.status == "inactive"

    async def test_activate_self_is_allowed(self):
        repo = AsyncMock()
        user_id = uuid4()
        user = _make_user(id=user_id, status="active")
        repo.update_status.return_value = user

        # activating self is allowed (only deactivating self is forbidden)
        result = await UpdateUserStatusUseCase(repo).execute(UpdateUserStatusCommand(
            user_id=user_id,
            organization_id=uuid4(),
            requesting_user_id=user_id,
            status="active",
        ))
        assert result.status == "active"
