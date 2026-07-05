from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, field_validator


class ProjectCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")
    name: str
    description: str | None = None
    owner_id: UUID

    @field_validator("name")
    @classmethod
    def name_not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Name cannot be empty")
        return v.strip()


class ProjectUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")
    name: str | None = None
    description: str | None = None
    owner_id: UUID | None = None
    status: str | None = None


class OwnerInfo(BaseModel):
    id: UUID
    full_name: str


class ProjectListItem(BaseModel):
    id: UUID
    name: str
    description: str | None = None
    status: str
    owner: OwnerInfo | None = None
    phases_count: int = 0
    members_count: int = 0
    created_at: datetime | None = None


class ProjectListResponse(BaseModel):
    items: list[ProjectListItem]
    total: int
    page: int
    page_size: int


class PhaseResponse(BaseModel):
    id: UUID
    name: str
    status: str


class MemberResponse(BaseModel):
    user_id: UUID
    full_name: str
    role: str


class ProjectDetailResponse(BaseModel):
    id: UUID
    name: str
    description: str | None = None
    status: str
    owner: OwnerInfo | None = None
    phases: list[PhaseResponse] = []
    members: list[MemberResponse] = []
    created_at: datetime | None = None
    updated_at: datetime | None = None


class PhaseCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")
    name: str

    @field_validator("name")
    @classmethod
    def name_not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Name cannot be empty")
        return v.strip()


class PhaseUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")
    name: str | None = None
    status: str | None = None


class MemberAdd(BaseModel):
    model_config = ConfigDict(extra="forbid")
    user_id: UUID


class AvailablePhaseItem(BaseModel):
    id: UUID
    name: str
    project_name: str
