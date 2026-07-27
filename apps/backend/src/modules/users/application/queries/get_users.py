from dataclasses import dataclass
from uuid import UUID

from src.modules.users.domain.entities.user_detail import UserDetail
from src.modules.users.domain.repositories.user_management_repository import UserManagementRepository


@dataclass
class GetUsersQuery:
    organization_id: UUID
    role: str | None = None
    status: str | None = None
    page: int = 1
    page_size: int = 20


@dataclass
class GetUsersResult:
    items: list[UserDetail]
    total: int
    page: int
    page_size: int


class GetUsersUseCase:
    def __init__(self, repo: UserManagementRepository) -> None:
        self._repo = repo

    async def execute(self, query: GetUsersQuery) -> GetUsersResult:
        items, total = await self._repo.list_users(
            organization_id=query.organization_id,
            role=query.role,
            status=query.status,
            page=query.page,
            page_size=query.page_size,
        )
        return GetUsersResult(items=items, total=total, page=query.page, page_size=query.page_size)


class GetUserByIdUseCase:
    def __init__(self, repo: UserManagementRepository) -> None:
        self._repo = repo

    async def execute(self, user_id: UUID, organization_id: UUID) -> UserDetail:
        user = await self._repo.get_by_id(user_id, organization_id)
        if user is None:
            raise ValueError(f"User {user_id} not found")
        return user
