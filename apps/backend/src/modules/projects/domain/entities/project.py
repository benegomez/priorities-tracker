from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime
from uuid import UUID

from src.shared.exceptions.base import BusinessRuleViolation

VALID_PROJECT_TRANSITIONS: dict[str, list[str]] = {
    "draft": ["active"],
    "active": ["on_hold", "completed"],
    "on_hold": ["active"],
    "completed": ["archived"],
    "archived": [],
}


@dataclass
class Project:
    id: UUID
    organization_id: UUID
    owner_id: UUID | None
    name: str
    description: str | None = None
    status: str = "draft"
    created_at: datetime | None = None
    updated_at: datetime | None = None

    def change_status(self, new_status: str) -> None:
        valid = VALID_PROJECT_TRANSITIONS.get(self.status, [])
        if new_status not in valid:
            raise BusinessRuleViolation(
                f"Invalid project transition: {self.status} → {new_status}. Valid: {valid}"
            )
        self.status = new_status
