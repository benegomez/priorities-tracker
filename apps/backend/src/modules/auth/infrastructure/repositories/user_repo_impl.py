from uuid import UUID

from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession

from src.modules.auth.domain.entities.user import User
from src.modules.auth.domain.repositories.user_repository import UserRepository


class UserRepositoryImpl(UserRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_email(self, email: str) -> User | None:
        query = select(
            text("id, organization_id, email, hashed_password, role, status, first_name, last_name")
        ).select_from(text("users")).where(
            text("email = :email AND deleted_at IS NULL")
        )
        result = await self._session.execute(query, {"email": email})
        row = result.one_or_none()
        if row is None:
            return None
        return self._to_entity(row)

    async def get_by_id(self, user_id: UUID) -> User | None:
        query = select(
            text("id, organization_id, email, hashed_password, role, status, first_name, last_name")
        ).select_from(text("users")).where(
            text("id = :user_id AND deleted_at IS NULL")
        )
        result = await self._session.execute(query, {"user_id": user_id})
        row = result.one_or_none()
        if row is None:
            return None
        return self._to_entity(row)

    @staticmethod
    def _to_entity(row) -> User:
        return User(
            id=row.id,
            organization_id=row.organization_id,
            email=row.email,
            hashed_password=row.hashed_password,
            role=row.role,
            status=row.status,
            first_name=row.first_name,
            last_name=row.last_name,
        )
