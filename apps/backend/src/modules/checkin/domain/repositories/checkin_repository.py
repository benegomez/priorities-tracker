from abc import ABC, abstractmethod
from datetime import date
from uuid import UUID

from src.modules.checkin.domain.entities.checkin import WeeklyCheckIn


class CheckInRepository(ABC):
    @abstractmethod
    async def save(self, checkin: WeeklyCheckIn) -> None: ...

    @abstractmethod
    async def get_by_id(self, checkin_id: UUID, organization_id: UUID) -> WeeklyCheckIn | None: ...

    @abstractmethod
    async def get_by_employee_and_week(
        self, employee_id: UUID, week_start: date, organization_id: UUID
    ) -> WeeklyCheckIn | None: ...

    @abstractmethod
    async def update(self, checkin: WeeklyCheckIn) -> None: ...
