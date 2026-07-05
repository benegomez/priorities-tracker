from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from src.shared.exceptions.base import BusinessRuleViolation

VALID_PHASE_TRANSITIONS: dict[str, list[str]] = {
    "planned": ["active", "cancelled"],
    "active": ["completed", "cancelled"],
    "completed": [],
    "cancelled": [],
}


@dataclass
class ProjectPhase:
    id: UUID
    organization_id: UUID
    project_id: UUID
    name: str
    status: str = "planned"
    created_at: datetime | None = None
    updated_at: datetime | None = None

    def change_status(self, new_status: str) -> None:
        valid = VALID_PHASE_TRANSITIONS.get(self.status, [])
        if new_status not in valid:
            raise BusinessRuleViolation(
                f"Invalid phase transition: {self.status} → {new_status}. Valid: {valid}"
            )
        self.status = new_status
