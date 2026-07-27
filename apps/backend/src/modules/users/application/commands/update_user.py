from dataclasses import dataclass
from uuid import UUID

from src.modules.users.domain.entities.user_detail import UserDetail
from src.modules.users.domain.repositories.user_management_repository import UserManagementRepository
from src.shared.exceptions.base import BusinessRuleViolation
from src.shared.security.password_service import PasswordService


@dataclass
class UpdateUserCommand:
    user_id: UUID
    organization_id: UUID
    requesting_user_id: UUID
    first_name: str | None
    last_name: str | None
    role: str | None
    manager_id: UUID | None
    new_password: str | None = None


class UpdateUserUseCase:
    def __init__(self, repo: UserManagementRepository) -> None:
        self._repo = repo

    async def execute(self, command: UpdateUserCommand) -> UserDetail:
        if command.role is not None and command.user_id == command.requesting_user_id:
            raise BusinessRuleViolation("BR-NEW-02: Administrator cannot change their own role")

        hashed_password = PasswordService.hash_password(command.new_password) if command.new_password else None

        user = await self._repo.update(
            user_id=command.user_id,
            organization_id=command.organization_id,
            first_name=command.first_name,
            last_name=command.last_name,
            role=command.role,
            manager_id=command.manager_id,
            hashed_password=hashed_password,
        )
        if user is None:
            raise ValueError(f"User {command.user_id} not found")
        return user


@dataclass
class UpdateUserStatusCommand:
    user_id: UUID
    organization_id: UUID
    requesting_user_id: UUID
    status: str


class UpdateUserStatusUseCase:
    def __init__(self, repo: UserManagementRepository) -> None:
        self._repo = repo

    async def execute(self, command: UpdateUserStatusCommand) -> UserDetail:
        if command.status == "inactive" and command.user_id == command.requesting_user_id:
            raise BusinessRuleViolation("BR-NEW-01: Administrator cannot deactivate their own account")

        user = await self._repo.update_status(
            user_id=command.user_id,
            organization_id=command.organization_id,
            status=command.status,
        )
        if user is None:
            raise ValueError(f"User {command.user_id} not found")
        return user
