from abc import ABC, abstractmethod
from uuid import UUID

from src.modules.teams.domain.entities.team import TeamDetail, TeamMemberDetail


class TeamAdminRepository(ABC):
    @abstractmethod
    async def list_teams(
        self, organization_id: UUID, page: int, page_size: int
    ) -> tuple[list[TeamDetail], int]: ...

    @abstractmethod
    async def get_by_id(self, team_id: UUID, organization_id: UUID) -> TeamDetail | None: ...

    @abstractmethod
    async def name_exists(self, name: str, organization_id: UUID, exclude_id: UUID | None = None) -> bool: ...

    @abstractmethod
    async def manager_valid(self, manager_id: UUID, organization_id: UUID) -> bool: ...

    @abstractmethod
    async def create(self, organization_id: UUID, name: str, manager_id: UUID | None) -> TeamDetail: ...

    @abstractmethod
    async def update(
        self, team_id: UUID, organization_id: UUID, name: str | None, manager_id: UUID | None
    ) -> TeamDetail | None: ...

    @abstractmethod
    async def get_members(self, team_id: UUID, organization_id: UUID) -> list[TeamMemberDetail]: ...

    @abstractmethod
    async def add_member(self, team_id: UUID, user_id: UUID, organization_id: UUID) -> bool: ...

    @abstractmethod
    async def remove_member(self, team_id: UUID, user_id: UUID, organization_id: UUID) -> bool: ...

    @abstractmethod
    async def user_exists(self, user_id: UUID, organization_id: UUID) -> bool: ...
