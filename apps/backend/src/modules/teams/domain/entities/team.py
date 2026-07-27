from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID


@dataclass
class TeamMemberDetail:
    id: UUID
    first_name: str
    last_name: str
    role: str
    status: str


@dataclass
class TeamDetail:
    id: UUID
    organization_id: UUID
    name: str
    manager_id: UUID | None
    manager_name: str | None
    member_count: int
    created_at: datetime | None = None
    updated_at: datetime | None = None
    members: list[TeamMemberDetail] = field(default_factory=list)
