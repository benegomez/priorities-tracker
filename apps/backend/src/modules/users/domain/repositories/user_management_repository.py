from abc import ABC, abstractmethod
from uuid import UUID

from src.modules.users.domain.entities.user_detail import UserDetail


class UserManagementRepository(ABC):
    @abstractmethod
    async def list_users(
        self,
        organization_id: UUID,
        role: str | None,
        status: str | None,
        page: int,
        page_size: int,
    ) -> tuple[list[UserDetail], int]: ...

    @abstractmethod
    async def get_by_id(self, user_id: UUID, organization_id: UUID) -> UserDetail | None: ...

    @abstractmethod
    async def email_exists(self, email: str, organization_id: UUID) -> bool: ...

    @abstractmethod
    async def manager_exists(self, manager_id: UUID, organization_id: UUID) -> bool: ...

    @abstractmethod
    async def create(
        self,
        organization_id: UUID,
        email: str,
        hashed_password: str,
        first_name: str,
        last_name: str,
        role: str,
        manager_id: UUID | None,
    ) -> UserDetail: ...

    @abstractmethod
    async def update(
        self,
        user_id: UUID,
        organization_id: UUID,
        first_name: str | None,
        last_name: str | None,
        role: str | None,
        manager_id: UUID | None,
    ) -> UserDetail | None: ...

    @abstractmethod
    async def update_status(
        self, user_id: UUID, organization_id: UUID, status: str
    ) -> UserDetail | None: ...
