from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from src.shared.exceptions.base import ValidationException


@dataclass
class Task:
    id: UUID
    organization_id: UUID
    priority_id: UUID
    title: str
    description: str | None = None
    status: str = "pending"
    created_at: datetime | None = None
    updated_at: datetime | None = None

    def __post_init__(self) -> None:
        if not self.title or not self.title.strip():
            raise ValidationException("Task title cannot be empty")
