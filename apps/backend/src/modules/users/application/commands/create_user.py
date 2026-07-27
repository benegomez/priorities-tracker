import secrets
import string
from dataclasses import dataclass
from uuid import UUID

from src.modules.users.domain.entities.user_detail import UserDetail
from src.modules.users.domain.repositories.user_management_repository import UserManagementRepository
from src.shared.exceptions.base import BusinessRuleViolation
from src.shared.security.password_service import PasswordService


def generate_temporary_password(length: int = 12) -> str:
    alphabet = string.ascii_letters + string.digits + "!@#$"
    password = [
        secrets.choice(string.ascii_uppercase),
        secrets.choice(string.digits),
        secrets.choice("!@#$"),
        *[secrets.choice(alphabet) for _ in range(length - 3)],
    ]
    secrets.SystemRandom().shuffle(password)
    return "".join(password)


@dataclass
class CreateUserCommand:
    organization_id: UUID
    email: str
    first_name: str
    last_name: str
    role: str
    manager_id: UUID | None


@dataclass
class CreateUserResult:
    user: UserDetail
    temporary_password: str


class CreateUserUseCase:
    def __init__(self, repo: UserManagementRepository) -> None:
        self._repo = repo

    async def execute(self, command: CreateUserCommand) -> CreateUserResult:
        if await self._repo.email_exists(command.email, command.organization_id):
            raise BusinessRuleViolation("BR-NEW-04: Email already exists in this organization")

        if command.manager_id and not await self._repo.manager_exists(command.manager_id, command.organization_id):
            raise ValueError(f"Manager {command.manager_id} not found in organization")

        temp_password = generate_temporary_password()
        hashed = PasswordService.hash_password(temp_password)

        user = await self._repo.create(
            organization_id=command.organization_id,
            email=command.email,
            hashed_password=hashed,
            first_name=command.first_name,
            last_name=command.last_name,
            role=command.role,
            manager_id=command.manager_id,
        )
        return CreateUserResult(user=user, temporary_password=temp_password)
