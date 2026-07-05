from dataclasses import dataclass
from uuid import UUID

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from src.modules.checkout.domain.repositories.checkout_repository import CheckOutRepository
from src.shared.exceptions.base import AuthorizationException, BusinessRuleViolation


@dataclass
class MarkTaskCommand:
    checkout_id: UUID
    task_id: UUID
    completed: bool
    employee_id: UUID
    organization_id: UUID


class MarkTaskCompletedUseCase:
    def __init__(self, checkout_repo: CheckOutRepository, session: AsyncSession) -> None:
        self._checkout_repo = checkout_repo
        self._session = session

    async def execute(self, command: MarkTaskCommand) -> None:
        checkout = await self._checkout_repo.get_by_id(command.checkout_id, command.organization_id)
        if checkout is None:
            raise BusinessRuleViolation("Check-out not found")
        if str(checkout.employee_id) != str(command.employee_id):
            raise AuthorizationException("BR-013: Cannot modify another employee's check-out")
        if not checkout.is_draft:
            raise BusinessRuleViolation("Cannot modify a submitted check-out")

        # Verify task belongs to a priority of the checkout's checkin
        result = await self._session.execute(
            text("""
                SELECT t.id FROM tasks t
                JOIN priorities p ON t.priority_id = p.id
                WHERE t.id = :task_id AND p.checkin_id = :checkin_id
                  AND t.organization_id = :organization_id AND t.deleted_at IS NULL
            """),
            {"task_id": command.task_id, "checkin_id": checkout.checkin_id, "organization_id": command.organization_id},
        )
        if result.one_or_none() is None:
            raise BusinessRuleViolation("Task not found or does not belong to this check-in")

        checkout_id_value = command.checkout_id if command.completed else None
        await self._session.execute(
            text("""
                UPDATE tasks SET completed_in_checkout = :checkout_id, updated_at = now()
                WHERE id = :task_id AND organization_id = :organization_id
            """),
            {"checkout_id": checkout_id_value, "task_id": command.task_id, "organization_id": command.organization_id},
        )
        await self._session.commit()
