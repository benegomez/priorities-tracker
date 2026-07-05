from dataclasses import dataclass
from uuid import UUID

from src.modules.checkin.domain.entities.checkin import WeeklyCheckIn
from src.modules.checkin.domain.repositories.checkin_repository import CheckInRepository
from src.modules.priorities.domain.repositories.priority_repository import PriorityRepository
from src.shared.exceptions.base import AuthorizationException, BusinessRuleViolation


@dataclass
class SubmitCheckInCommand:
    checkin_id: UUID
    employee_id: UUID
    organization_id: UUID


class SubmitCheckInUseCase:
    def __init__(self, checkin_repo: CheckInRepository, priority_repo: PriorityRepository) -> None:
        self._checkin_repo = checkin_repo
        self._priority_repo = priority_repo

    async def execute(self, command: SubmitCheckInCommand) -> WeeklyCheckIn:
        checkin = await self._checkin_repo.get_by_id(command.checkin_id, command.organization_id)
        if checkin is None:
            raise BusinessRuleViolation("Check-in not found")

        # BR-013: employee can only submit their own check-in
        if checkin.employee_id != command.employee_id:
            raise AuthorizationException("Cannot submit another employee's check-in")

        # Count priorities for this check-in
        priorities_count = await self._priority_repo.count_by_checkin(
            checkin_id=command.checkin_id, organization_id=command.organization_id
        )

        # Domain entity validates state transition + minimum priorities
        checkin.submit(priorities_count)

        # Transition priorities to planned
        await self._priority_repo.transition_to_planned(
            checkin_id=command.checkin_id, organization_id=command.organization_id
        )

        await self._checkin_repo.update(checkin)
        return checkin
