from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class CheckInCreate(BaseModel):
    model_config = ConfigDict(extra="forbid", json_schema_extra={
        "example": {"week_start": "2025-01-06"}
    })

    week_start: date


class CheckInTaskItem(BaseModel):
    id: UUID
    title: str
    status: str


class CheckInPriorityItem(BaseModel):
    id: UUID
    title: str
    description: str | None = None
    priority_level: str
    status: str
    phase_name: str | None = None
    project_name: str | None = None
    tasks: list[CheckInTaskItem] = []


class CheckInResponse(BaseModel):
    id: UUID
    employee_id: UUID
    organization_id: UUID
    week_start: date
    status: str
    submitted_at: datetime | None = None
    priorities_count: int = 0
    priorities: list[CheckInPriorityItem] = []
    created_at: datetime | None = None
    updated_at: datetime | None = None


class CheckInSubmitResponse(BaseModel):
    id: UUID
    status: str
    submitted_at: datetime | None = None
