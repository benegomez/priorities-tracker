from dataclasses import dataclass
from uuid import UUID


@dataclass
class User:
    id: UUID
    organization_id: UUID
    email: str
    hashed_password: str
    role: str
    status: str
    first_name: str
    last_name: str

    def is_active(self) -> bool:
        return self.status == "active"

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"
