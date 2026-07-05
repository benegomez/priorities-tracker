from dataclasses import dataclass
from datetime import date, timedelta
from uuid import UUID

from src.modules.checkin.domain.entities.checkin import WeeklyCheckIn
from src.modules.checkin.domain.repositories.checkin_repository import CheckInRepository
from src.shared.config.settings import settings


@dataclass
class GetCurrentCheckInQuery:
    employee_id: UUID
    organization_id: UUID


class GetCurrentCheckInUseCase:
    def __init__(self, checkin_repo: CheckInRepository) -> None:
        self._checkin_repo = checkin_repo

    async def execute(self, query: GetCurrentCheckInQuery) -> WeeklyCheckIn | None:
        today = date.today()

        if settings.is_development:
            # In dev, search by today's date first, then fall back to Monday
            result = await self._checkin_repo.get_by_employee_and_week(
                employee_id=query.employee_id,
                week_start=today,
                organization_id=query.organization_id,
            )
            if result:
                return result

        # Production: always search by Monday of current week
        monday = today - timedelta(days=today.weekday())
        return await self._checkin_repo.get_by_employee_and_week(
            employee_id=query.employee_id,
            week_start=monday,
            organization_id=query.organization_id,
        )
