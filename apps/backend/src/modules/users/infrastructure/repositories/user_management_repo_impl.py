from uuid import UUID, uuid4

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from src.modules.users.domain.entities.user_detail import UserDetail
from src.modules.users.domain.repositories.user_management_repository import UserManagementRepository


class UserManagementRepoImpl(UserManagementRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_users(
        self,
        organization_id: UUID,
        role: str | None,
        status: str | None,
        page: int,
        page_size: int,
    ) -> tuple[list[UserDetail], int]:
        filters = "u.organization_id = :org_id AND u.deleted_at IS NULL"
        params: dict = {"org_id": organization_id}
        if role:
            filters += " AND u.role = :role"
            params["role"] = role
        if status:
            filters += " AND u.status = :status"
            params["status"] = status

        count_result = await self._session.execute(
            text(f"SELECT COUNT(*) FROM users u WHERE {filters}"), params
        )
        total = count_result.scalar_one()

        params["limit"] = page_size
        params["offset"] = (page - 1) * page_size
        result = await self._session.execute(
            text(f"""
                SELECT u.id, u.organization_id, u.manager_id, u.email, u.role, u.status,
                       u.first_name, u.last_name, u.created_at, u.updated_at,
                       m.first_name || ' ' || m.last_name AS manager_name
                FROM users u
                LEFT JOIN users m ON u.manager_id = m.id AND m.deleted_at IS NULL
                WHERE {filters}
                ORDER BY u.first_name, u.last_name
                LIMIT :limit OFFSET :offset
            """),
            params,
        )
        rows = result.fetchall()
        return [self._to_entity(r) for r in rows], total

    async def get_by_id(self, user_id: UUID, organization_id: UUID) -> UserDetail | None:
        result = await self._session.execute(
            text("""
                SELECT u.id, u.organization_id, u.manager_id, u.email, u.role, u.status,
                       u.first_name, u.last_name, u.created_at, u.updated_at,
                       m.first_name || ' ' || m.last_name AS manager_name
                FROM users u
                LEFT JOIN users m ON u.manager_id = m.id AND m.deleted_at IS NULL
                WHERE u.id = :id AND u.organization_id = :org_id AND u.deleted_at IS NULL
            """),
            {"id": user_id, "org_id": organization_id},
        )
        row = result.one_or_none()
        return self._to_entity(row) if row else None

    async def email_exists(self, email: str, organization_id: UUID) -> bool:
        result = await self._session.execute(
            text("SELECT 1 FROM users WHERE email = :email AND organization_id = :org_id AND deleted_at IS NULL"),
            {"email": email, "org_id": organization_id},
        )
        return result.one_or_none() is not None

    async def manager_exists(self, manager_id: UUID, organization_id: UUID) -> bool:
        result = await self._session.execute(
            text("SELECT 1 FROM users WHERE id = :id AND organization_id = :org_id AND deleted_at IS NULL"),
            {"id": manager_id, "org_id": organization_id},
        )
        return result.one_or_none() is not None

    async def create(
        self,
        organization_id: UUID,
        email: str,
        hashed_password: str,
        first_name: str,
        last_name: str,
        role: str,
        manager_id: UUID | None,
    ) -> UserDetail:
        new_id = uuid4()
        await self._session.execute(
            text("""
                INSERT INTO users (id, organization_id, manager_id, email, hashed_password,
                                   role, status, first_name, last_name)
                VALUES (:id, :org_id, :manager_id, :email, :hashed_password,
                        :role, 'active', :first_name, :last_name)
            """),
            {
                "id": new_id,
                "org_id": organization_id,
                "manager_id": manager_id,
                "email": email,
                "hashed_password": hashed_password,
                "role": role,
                "first_name": first_name,
                "last_name": last_name,
            },
        )
        await self._session.flush()
        user = await self.get_by_id(new_id, organization_id)
        return user  # type: ignore[return-value]

    async def update(
        self,
        user_id: UUID,
        organization_id: UUID,
        first_name: str | None,
        last_name: str | None,
        role: str | None,
        manager_id: UUID | None,
    ) -> UserDetail | None:
        await self._session.execute(
            text("""
                UPDATE users SET
                    first_name = COALESCE(:first_name, first_name),
                    last_name  = COALESCE(:last_name, last_name),
                    role       = COALESCE(:role, role),
                    manager_id = COALESCE(CAST(:manager_id AS uuid), manager_id),
                    updated_at = now()
                WHERE id = :id AND organization_id = :org_id AND deleted_at IS NULL
            """),
            {
                "id": user_id,
                "org_id": organization_id,
                "first_name": first_name,
                "last_name": last_name,
                "role": role,
                "manager_id": manager_id,
            },
        )
        await self._session.flush()
        return await self.get_by_id(user_id, organization_id)

    async def update_status(self, user_id: UUID, organization_id: UUID, status: str) -> UserDetail | None:
        await self._session.execute(
            text("""
                UPDATE users SET status = :status, updated_at = now()
                WHERE id = :id AND organization_id = :org_id AND deleted_at IS NULL
            """),
            {"id": user_id, "org_id": organization_id, "status": status},
        )
        await self._session.flush()
        return await self.get_by_id(user_id, organization_id)

    @staticmethod
    def _to_entity(row) -> UserDetail:
        return UserDetail(
            id=row.id,
            organization_id=row.organization_id,
            manager_id=row.manager_id,
            email=row.email,
            role=row.role,
            status=row.status,
            first_name=row.first_name,
            last_name=row.last_name,
            manager_name=row.manager_name,
        )
