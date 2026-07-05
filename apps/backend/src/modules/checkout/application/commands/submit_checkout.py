from dataclasses import dataclass
from uuid import UUID
import logging

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from src.modules.checkout.domain.repositories.checkout_repository import CheckOutRepository
from src.shared.exceptions.base import AuthorizationException, BusinessRuleViolation

logger = logging.getLogger(__name__)


@dataclass
class SubmitCheckOutCommand:
    checkout_id: UUID
    employee_id: UUID
    organization_id: UUID
    notes: str | None = None
    lessons_learned: str | None = None


@dataclass
class CheckOutSummary:
    priorities_total: int
    priorities_completed: int
    priorities_carried: int
    tasks_total: int
    tasks_completed: int


class SubmitCheckOutUseCase:
    def __init__(self, checkout_repo: CheckOutRepository, session: AsyncSession) -> None:
        self._checkout_repo = checkout_repo
        self._session = session

    async def execute(self, command: SubmitCheckOutCommand) -> tuple:
        checkout = await self._checkout_repo.get_by_id(command.checkout_id, command.organization_id)
        if checkout is None:
            raise BusinessRuleViolation("Check-out not found")
        if str(checkout.employee_id) != str(command.employee_id):
            raise AuthorizationException("BR-013: Cannot submit another employee's check-out")

        # Transition checkout
        checkout.submit(notes=command.notes, lessons_learned=command.lessons_learned)

        # Transition priorities: completed_in_checkout set → completed, else → carried_over
        await self._session.execute(
            text("""
                UPDATE priorities SET status = 'completed', updated_at = now()
                WHERE checkin_id = :checkin_id AND completed_in_checkout = :checkout_id
                  AND organization_id = :organization_id AND deleted_at IS NULL
            """),
            {"checkin_id": checkout.checkin_id, "checkout_id": checkout.id, "organization_id": command.organization_id},
        )
        await self._session.execute(
            text("""
                UPDATE priorities SET status = 'carried_over', updated_at = now()
                WHERE checkin_id = :checkin_id AND (completed_in_checkout IS NULL OR completed_in_checkout != :checkout_id)
                  AND organization_id = :organization_id AND deleted_at IS NULL
                  AND status NOT IN ('completed')
            """),
            {"checkin_id": checkout.checkin_id, "checkout_id": checkout.id, "organization_id": command.organization_id},
        )

        # Transition tasks: completed_in_checkout set → completed, else → cancelled
        await self._session.execute(
            text("""
                UPDATE tasks SET status = 'completed', updated_at = now()
                WHERE priority_id IN (SELECT id FROM priorities WHERE checkin_id = :checkin_id AND organization_id = :organization_id AND deleted_at IS NULL)
                  AND completed_in_checkout = :checkout_id
                  AND organization_id = :organization_id AND deleted_at IS NULL
            """),
            {"checkin_id": checkout.checkin_id, "checkout_id": checkout.id, "organization_id": command.organization_id},
        )
        await self._session.execute(
            text("""
                UPDATE tasks SET status = 'cancelled', updated_at = now()
                WHERE priority_id IN (SELECT id FROM priorities WHERE checkin_id = :checkin_id AND organization_id = :organization_id AND deleted_at IS NULL)
                  AND (completed_in_checkout IS NULL OR completed_in_checkout != :checkout_id)
                  AND organization_id = :organization_id AND deleted_at IS NULL
                  AND status NOT IN ('completed')
            """),
            {"checkin_id": checkout.checkin_id, "checkout_id": checkout.id, "organization_id": command.organization_id},
        )

        # Update checkout
        await self._checkout_repo.update(checkout)

        # Calculate summary
        result = await self._session.execute(
            text("""
                SELECT
                    COUNT(*) as total,
                    COUNT(*) FILTER (WHERE status = 'completed') as completed,
                    COUNT(*) FILTER (WHERE status = 'carried_over') as carried
                FROM priorities
                WHERE checkin_id = :checkin_id AND organization_id = :organization_id AND deleted_at IS NULL
            """),
            {"checkin_id": checkout.checkin_id, "organization_id": command.organization_id},
        )
        p = result.one()

        result = await self._session.execute(
            text("""
                SELECT
                    COUNT(*) as total,
                    COUNT(*) FILTER (WHERE status = 'completed') as completed
                FROM tasks
                WHERE priority_id IN (SELECT id FROM priorities WHERE checkin_id = :checkin_id AND organization_id = :organization_id AND deleted_at IS NULL)
                  AND organization_id = :organization_id AND deleted_at IS NULL
            """),
            {"checkin_id": checkout.checkin_id, "organization_id": command.organization_id},
        )
        t = result.one()

        summary = CheckOutSummary(
            priorities_total=p.total,
            priorities_completed=p.completed,
            priorities_carried=p.carried,
            tasks_total=t.total,
            tasks_completed=t.completed,
        )

        # CRS calculation (best-effort)
        try:
            logger.info("CRS calculation triggered for employee=%s week=%s", command.employee_id, checkout.week_start)
            # TODO: invoke CRS module when implemented
        except Exception as e:
            logger.warning("CRS calculation failed (best-effort): %s", e)

        return checkout, summary
