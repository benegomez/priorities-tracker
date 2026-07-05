from abc import ABC, abstractmethod
from uuid import UUID

from src.modules.priorities.domain.entities.priority import Priority


class PriorityRepository(ABC):
    @abstractmethod
    async def save(self, priority: Priority) -> None: ...

    @abstractmethod
    async def get_by_id(self, priority_id: UUID, organization_id: UUID) -> Priority | None: ...

    @abstractmethod
    async def count_by_checkin(self, checkin_id: UUID, organization_id: UUID) -> int: ...

    @abstractmethod
    async def transition_to_planned(self, checkin_id: UUID, organization_id: UUID) -> None: ...
