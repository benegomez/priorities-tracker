from dataclasses import dataclass
from uuid import UUID, uuid4

from src.modules.priorities.domain.entities.task import Task
from src.modules.priorities.domain.repositories.priority_repository import PriorityRepository
from src.modules.priorities.domain.repositories.task_repository import TaskRepository
from src.shared.exceptions.base import AuthorizationException, BusinessRuleViolation


@dataclass
class CreateTaskCommand:
    priority_id: UUID
    title: str
    description: str | None
    employee_id: UUID
    organization_id: UUID


class CreateTaskUseCase:
    def __init__(self, task_repo: TaskRepository, priority_repo: PriorityRepository) -> None:
        self._task_repo = task_repo
        self._priority_repo = priority_repo

    async def execute(self, command: CreateTaskCommand) -> Task:
        # BR-005: task must belong to a priority
        priority = await self._priority_repo.get_by_id(command.priority_id, command.organization_id)
        if priority is None:
            raise BusinessRuleViolation("BR-005: Priority not found")

        # BR-013: employee can only add tasks to their own priorities
        if priority.owner_id != command.employee_id:
            raise AuthorizationException("BR-013: Cannot add tasks to another employee's priority")

        task = Task(
            id=uuid4(),
            organization_id=command.organization_id,
            priority_id=command.priority_id,
            title=command.title,
            description=command.description,
        )

        await self._task_repo.save(task)
        return task
