from dataclasses import dataclass
from datetime import datetime, timezone
from uuid import UUID


@dataclass
class RefreshToken:
    id: UUID
    user_id: UUID
    token_hash: str
    expires_at: datetime
    revoked_at: datetime | None = None

    def is_valid(self) -> bool:
        if self.revoked_at is not None:
            return False
        return datetime.now(timezone.utc) < self.expires_at
