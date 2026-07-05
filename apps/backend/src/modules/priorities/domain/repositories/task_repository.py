from abc import ABC, abstractmethod
from uuid import UUID

from src.modules.priorities.domain.entities.task import Task


class TaskRepository(ABC):
    @abstractmethod
    async def save(self, task: Task) -> None: ...

    @abstractmethod
    async def get_by_id(self, task_id: UUID, organization_id: UUID) -> Task | None: ...
