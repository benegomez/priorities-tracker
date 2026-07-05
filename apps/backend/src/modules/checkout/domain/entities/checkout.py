from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, date, datetime
from uuid import UUID

from src.shared.exceptions.base import BusinessRuleViolation


@dataclass
class WeeklyCheckOut:
    id: UUID
    organization_id: UUID
    employee_id: UUID
    checkin_id: UUID
    week_start: date
    status: str = "draft"
    submitted_at: datetime | None = None
    notes: str | None = None
    lessons_learned: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    def submit(self, notes: str | None = None, lessons_learned: str | None = None) -> None:
        if self.status != "draft":
            raise BusinessRuleViolation("Check-out can only be submitted from draft status")
        self.status = "submitted"
        self.submitted_at = datetime.now(UTC)
        self.notes = notes
        self.lessons_learned = lessons_learned

    @property
    def is_draft(self) -> bool:
        return self.status == "draft"
