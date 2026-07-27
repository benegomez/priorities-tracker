from dataclasses import dataclass
from uuid import UUID


@dataclass
class UserDetail:
    id: UUID
    organization_id: UUID
    manager_id: UUID | None
    email: str
    role: str
    status: str
    first_name: str
    last_name: str
    manager_name: str | None = None

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"
