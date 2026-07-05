from dataclasses import dataclass
from uuid import UUID, uuid4

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from src.modules.checkout.domain.entities.checkout import WeeklyCheckOut
from src.modules.checkout.domain.repositories.checkout_repository import CheckOutRepository
from src.shared.exceptions.base import AuthorizationException, BusinessRuleViolation


@dataclass
class CreateCheckOutCommand:
    checkin_id: UUID
    employee_id: UUID
    organization_id: UUID


class CreateCheckOutUseCase:
    def __init__(self, checkout_repo: CheckOutRepository, session: AsyncSession) -> None:
        self._checkout_repo = checkout_repo
        self._session = session

    async def execute(self, command: CreateCheckOutCommand) -> WeeklyCheckOut:
        # Validate checkin exists, is submitted, and belongs to employee
        result = await self._session.execute(
            text("""
                SELECT id, employee_id, organization_id, week_start, status
                FROM check_ins
                WHERE id = :id AND deleted_at IS NULL
            """),
            {"id": command.checkin_id},
        )
        checkin = result.one_or_none()

        if checkin is None:
            raise BusinessRuleViolation("Check-in not found")

        if str(checkin.employee_id) != str(command.employee_id):
            raise AuthorizationException("BR-013: Cannot create check-out for another employee's check-in")

        if str(checkin.organization_id) != str(command.organization_id):
            raise AuthorizationException("BR-016: Cross-tenant access denied")

        if checkin.status != "submitted":
            raise BusinessRuleViolation("Check-in must be in submitted status to create a check-out")

        # BR-002: one checkout per employee per week
        existing = await self._checkout_repo.get_by_employee_and_week(
            employee_id=command.employee_id,
            week_start=checkin.week_start,
            organization_id=command.organization_id,
        )
        if existing is not None:
            raise BusinessRuleViolation("BR-002: A check-out already exists for this employee and week")

        checkout = WeeklyCheckOut(
            id=uuid4(),
            organization_id=command.organization_id,
            employee_id=command.employee_id,
            checkin_id=command.checkin_id,
            week_start=checkin.week_start,
        )

        await self._checkout_repo.save(checkout)
        return checkout
