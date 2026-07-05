from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, field_validator


class PriorityCreate(BaseModel):
    model_config = ConfigDict(extra="forbid", json_schema_extra={
        "example": {
            "checkin_id": "550e8400-e29b-41d4-a716-446655440000",
            "phase_id": "550e8400-e29b-41d4-a716-446655440001",
            "title": "Complete architecture design",
            "description": "Review and approve the technical design",
            "priority_level": "high",
        }
    })

    checkin_id: UUID
    phase_id: UUID
    title: str
    description: str | None = None
    priority_level: str = "medium"

    @field_validator("title")
    @classmethod
    def title_not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Title cannot be empty")
        return v.strip()

    @field_validator("priority_level")
    @classmethod
    def valid_level(cls, v: str) -> str:
        if v not in ("low", "medium", "high"):
            raise ValueError("priority_level must be low, medium, or high")
        return v


class PriorityResponse(BaseModel):
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "id": "550e8400-e29b-41d4-a716-446655440000",
            "checkin_id": "550e8400-e29b-41d4-a716-446655440001",
            "phase_id": "550e8400-e29b-41d4-a716-446655440002",
            "owner_id": "550e8400-e29b-41d4-a716-446655440003",
            "organization_id": "550e8400-e29b-41d4-a716-446655440004",
            "title": "Complete architecture design",
            "description": "Review and approve the technical design",
            "priority_level": "high",
            "status": "draft",
            "week_start": "2025-01-06",
            "created_at": "2025-01-06T08:00:00Z",
            "updated_at": "2025-01-06T08:00:00Z",
        }
    })

    id: UUID
    checkin_id: UUID
    phase_id: UUID
    owner_id: UUID
    organization_id: UUID
    title: str
    description: str | None = None
    priority_level: str
    status: str
    week_start: date
    created_at: datetime | None = None
    updated_at: datetime | None = None


class TaskCreate(BaseModel):
    model_config = ConfigDict(extra="forbid", json_schema_extra={
        "example": {"title": "Review JWT documentation", "description": None}
    })

    title: str
    description: str | None = None

    @field_validator("title")
    @classmethod
    def title_not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Title cannot be empty")
        return v.strip()


class TaskResponse(BaseModel):
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "id": "550e8400-e29b-41d4-a716-446655440000",
            "priority_id": "550e8400-e29b-41d4-a716-446655440001",
            "organization_id": "550e8400-e29b-41d4-a716-446655440002",
            "title": "Review JWT documentation",
            "description": None,
            "status": "pending",
            "created_at": "2025-01-06T08:00:00Z",
            "updated_at": "2025-01-06T08:00:00Z",
        }
    })

    id: UUID
    priority_id: UUID
    organization_id: UUID
    title: str
    description: str | None = None
    status: str
    created_at: datetime | None = None
    updated_at: datetime | None = None
