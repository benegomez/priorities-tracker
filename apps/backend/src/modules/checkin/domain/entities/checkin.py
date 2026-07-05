from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, date, datetime
from uuid import UUID

from src.shared.config.settings import settings
from src.shared.exceptions.base import BusinessRuleViolation, ValidationException


@dataclass
class WeeklyCheckIn:
    id: UUID
    organization_id: UUID
    employee_id: UUID
    week_start: date
    status: str = "draft"
    submitted_at: datetime | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    def __post_init__(self) -> None:
        self._validate_week_start()

    def _validate_week_start(self) -> None:
        if settings.is_development:
            return
        if self.week_start.weekday() != 0:
            raise ValidationException("week_start must be a Monday (ISO weekday 0)")

    def submit(self, priorities_count: int) -> None:
        if self.status not in ("draft", "submitted"):
            raise BusinessRuleViolation("Check-in can only be submitted from draft or submitted status")
        if priorities_count < 1:
            raise BusinessRuleViolation("Check-in must have at least one priority to be submitted")
        self.status = "submitted"
        self.submitted_at = datetime.now(UTC)

    @property
    def is_draft(self) -> bool:
        return self.status == "draft"
