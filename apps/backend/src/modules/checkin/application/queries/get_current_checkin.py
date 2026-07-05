from dataclasses import dataclass
from datetime import date
from uuid import UUID

from src.modules.checkin.domain.entities.checkin import WeeklyCheckIn
from src.modules.checkin.domain.repositories.checkin_repository import CheckInRepository


@dataclass
class GetCurrentCheckInQuery:
    employee_id: UUID
    organization_id: UUID


class GetCurrentCheckInUseCase:
    def __init__(self, checkin_repo: CheckInRepository) -> None:
        self._checkin_repo = checkin_repo

    async def execute(self, query: GetCurrentCheckInQuery) -> WeeklyCheckIn | None:
        today = date.today()
        # Calculate Monday of current week (ISO: Monday = 0)
        monday = today - __import__("datetime").timedelta(days=today.weekday())

        return await self._checkin_repo.get_by_employee_and_week(
            employee_id=query.employee_id,
            week_start=monday,
            organization_id=query.organization_id,
        )
