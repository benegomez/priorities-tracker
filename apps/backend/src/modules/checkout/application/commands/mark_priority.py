from dataclasses import dataclass
from uuid import UUID

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from src.modules.checkout.domain.repositories.checkout_repository import CheckOutRepository
from src.shared.exceptions.base import AuthorizationException, BusinessRuleViolation


@dataclass
class MarkPriorityCommand:
    checkout_id: UUID
    priority_id: UUID
    completed: bool
    employee_id: UUID
    organization_id: UUID


class MarkPriorityCompletedUseCase:
    def __init__(self, checkout_repo: CheckOutRepository, session: AsyncSession) -> None:
        self._checkout_repo = checkout_repo
        self._session = session

    async def execute(self, command: MarkPriorityCommand) -> None:
        checkout = await self._checkout_repo.get_by_id(command.checkout_id, command.organization_id)
        if checkout is None:
            raise BusinessRuleViolation("Check-out not found")
        if str(checkout.employee_id) != str(command.employee_id):
            raise AuthorizationException("BR-013: Cannot modify another employee's check-out")
        if not checkout.is_draft:
            raise BusinessRuleViolation("Cannot modify a submitted check-out")

        # Verify priority belongs to the checkout's checkin
        result = await self._session.execute(
            text("""
                SELECT id FROM priorities
                WHERE id = :priority_id AND checkin_id = :checkin_id
                  AND organization_id = :organization_id AND deleted_at IS NULL
            """),
            {"priority_id": command.priority_id, "checkin_id": checkout.checkin_id, "organization_id": command.organization_id},
        )
        if result.one_or_none() is None:
            raise BusinessRuleViolation("BR-008: Priority not found or does not belong to this check-in")

        # Update completed_in_checkout
        checkout_id_value = command.checkout_id if command.completed else None
        await self._session.execute(
            text("""
                UPDATE priorities SET completed_in_checkout = :checkout_id, updated_at = now()
                WHERE id = :priority_id AND organization_id = :organization_id
            """),
            {"checkout_id": checkout_id_value, "priority_id": command.priority_id, "organization_id": command.organization_id},
        )
        await self._session.commit()
