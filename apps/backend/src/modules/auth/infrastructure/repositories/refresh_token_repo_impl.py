from datetime import datetime, timezone

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from src.modules.auth.domain.value_objects.refresh_token import RefreshToken
from src.modules.auth.domain.repositories.refresh_token_repository import RefreshTokenRepository


class RefreshTokenRepositoryImpl(RefreshTokenRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def save(self, token: RefreshToken) -> None:
        await self._session.execute(
            text("""
                INSERT INTO refresh_tokens (id, user_id, token_hash, expires_at)
                VALUES (:id, :user_id, :token_hash, :expires_at)
            """),
            {
                "id": token.id,
                "user_id": token.user_id,
                "token_hash": token.token_hash,
                "expires_at": token.expires_at,
            },
        )
        await self._session.commit()

    async def get_by_hash(self, token_hash: str) -> RefreshToken | None:
        result = await self._session.execute(
            text("""
                SELECT id, user_id, token_hash, expires_at, revoked_at
                FROM refresh_tokens
                WHERE token_hash = :token_hash
            """),
            {"token_hash": token_hash},
        )
        row = result.one_or_none()
        if row is None:
            return None
        return RefreshToken(
            id=row.id,
            user_id=row.user_id,
            token_hash=row.token_hash,
            expires_at=row.expires_at,
            revoked_at=row.revoked_at,
        )

    async def revoke(self, token_hash: str) -> None:
        await self._session.execute(
            text("""
                UPDATE refresh_tokens
                SET revoked_at = :now
                WHERE token_hash = :token_hash AND revoked_at IS NULL
            """),
            {"token_hash": token_hash, "now": datetime.now(timezone.utc)},
        )
        await self._session.commit()
