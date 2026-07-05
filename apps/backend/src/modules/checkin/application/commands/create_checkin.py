from dataclasses import dataclass
from datetime import date
from uuid import UUID, uuid4

from src.modules.checkin.domain.entities.checkin import WeeklyCheckIn
from src.modules.checkin.domain.repositories.checkin_repository import CheckInRepository
from src.shared.exceptions.base import BusinessRuleViolation


@dataclass
class CreateCheckInCommand:
    employee_id: UUID
    organization_id: UUID
    week_start: date


class CreateCheckInUseCase:
    def __init__(self, checkin_repo: CheckInRepository) -> None:
        self._checkin_repo = checkin_repo

    async def execute(self, command: CreateCheckInCommand) -> WeeklyCheckIn:
        # BR-001: one check-in per employee per week
        existing = await self._checkin_repo.get_by_employee_and_week(
            employee_id=command.employee_id,
            week_start=command.week_start,
            organization_id=command.organization_id,
        )
        if existing is not None:
            raise BusinessRuleViolation("BR-001: A check-in already exists for this employee and week")

        checkin = WeeklyCheckIn(
            id=uuid4(),
            organization_id=command.organization_id,
            employee_id=command.employee_id,
            week_start=command.week_start,
        )

        await self._checkin_repo.save(checkin)
        return checkin
