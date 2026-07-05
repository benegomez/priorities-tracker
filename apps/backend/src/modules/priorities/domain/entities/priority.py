from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime
from uuid import UUID

from src.shared.exceptions.base import ValidationException

VALID_PRIORITY_LEVELS = ("low", "medium", "high")


@dataclass
class Priority:
    id: UUID
    organization_id: UUID
    checkin_id: UUID
    phase_id: UUID
    owner_id: UUID
    week_start: date
    title: str
    description: str | None = None
    priority_level: str = "medium"
    status: str = "draft"
    created_at: datetime | None = None
    updated_at: datetime | None = None

    def __post_init__(self) -> None:
        if not self.title or not self.title.strip():
            raise ValidationException("Priority title cannot be empty")
        if self.priority_level not in VALID_PRIORITY_LEVELS:
            raise ValidationException(f"priority_level must be one of {VALID_PRIORITY_LEVELS}")

    def transition_to_planned(self) -> None:
        self.status = "planned"
