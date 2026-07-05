from dataclasses import dataclass
from datetime import date, timedelta
from uuid import UUID

from src.modules.checkout.domain.entities.checkout import WeeklyCheckOut
from src.modules.checkout.domain.repositories.checkout_repository import CheckOutRepository
from src.shared.config.settings import settings


@dataclass
class GetCurrentCheckOutQuery:
    employee_id: UUID
    organization_id: UUID


class GetCurrentCheckOutUseCase:
    def __init__(self, checkout_repo: CheckOutRepository) -> None:
        self._checkout_repo = checkout_repo

    async def execute(self, query: GetCurrentCheckOutQuery) -> WeeklyCheckOut | None:
        today = date.today()

        if settings.is_development:
            result = await self._checkout_repo.get_by_employee_and_week(
                employee_id=query.employee_id, week_start=today, organization_id=query.organization_id
            )
            if result:
                return result

        monday = today - timedelta(days=today.weekday())
        return await self._checkout_repo.get_by_employee_and_week(
            employee_id=query.employee_id, week_start=monday, organization_id=query.organization_id
        )
