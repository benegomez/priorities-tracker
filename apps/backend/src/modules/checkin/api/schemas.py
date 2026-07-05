from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class CheckInCreate(BaseModel):
    model_config = ConfigDict(extra="forbid", json_schema_extra={
        "example": {"week_start": "2025-01-06"}
    })

    week_start: date


class CheckInResponse(BaseModel):
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "id": "550e8400-e29b-41d4-a716-446655440000",
            "employee_id": "550e8400-e29b-41d4-a716-446655440001",
            "organization_id": "550e8400-e29b-41d4-a716-446655440002",
            "week_start": "2025-01-06",
            "status": "draft",
            "submitted_at": None,
            "created_at": "2025-01-06T08:00:00Z",
            "updated_at": "2025-01-06T08:00:00Z",
        }
    })

    id: UUID
    employee_id: UUID
    organization_id: UUID
    week_start: date
    status: str
    submitted_at: datetime | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


class CheckInSubmitResponse(BaseModel):
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "id": "550e8400-e29b-41d4-a716-446655440000",
            "status": "submitted",
            "submitted_at": "2025-01-06T08:30:00Z",
        }
    })

    id: UUID
    status: str
    submitted_at: datetime | None = None
