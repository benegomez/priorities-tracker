from abc import ABC, abstractmethod
from datetime import date
from uuid import UUID

from src.modules.checkout.domain.entities.checkout import WeeklyCheckOut


class CheckOutRepository(ABC):
    @abstractmethod
    async def save(self, checkout: WeeklyCheckOut) -> None: ...

    @abstractmethod
    async def get_by_id(self, checkout_id: UUID, organization_id: UUID) -> WeeklyCheckOut | None: ...

    @abstractmethod
    async def get_by_employee_and_week(self, employee_id: UUID, week_start: date, organization_id: UUID) -> WeeklyCheckOut | None: ...

    @abstractmethod
    async def update(self, checkout: WeeklyCheckOut) -> None: ...
