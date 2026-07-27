from uuid import UUID, uuid4

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from src.modules.teams.domain.entities.team import TeamDetail, TeamMemberDetail
from src.modules.teams.domain.repositories.team_admin_repository import TeamAdminRepository


class TeamAdminRepoImpl(TeamAdminRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_teams(
        self, organization_id: UUID, page: int, page_size: int
    ) -> tuple[list[TeamDetail], int]:
        params: dict = {"org_id": organization_id}

        count_result = await self._session.execute(
            text("SELECT COUNT(*) FROM teams WHERE organization_id = :org_id AND deleted_at IS NULL"),
            params,
        )
        total = count_result.scalar_one()

        params["limit"] = page_size
        params["offset"] = (page - 1) * page_size
        result = await self._session.execute(
            text("""
                SELECT t.id, t.name, t.manager_id, t.organization_id, t.created_at, t.updated_at,
                       u.first_name || ' ' || u.last_name AS manager_name,
                       COUNT(m.id) FILTER (WHERE m.deleted_at IS NULL) AS member_count
                FROM teams t
                LEFT JOIN users u ON t.manager_id = u.id AND u.deleted_at IS NULL
                LEFT JOIN users m ON m.team_id = t.id
                WHERE t.organization_id = :org_id AND t.deleted_at IS NULL
                GROUP BY t.id, t.name, t.manager_id, t.organization_id, t.created_at, t.updated_at,
                         u.first_name, u.last_name
                ORDER BY t.name
                LIMIT :limit OFFSET :offset
            """),
            params,
        )
        rows = result.fetchall()
        return [self._to_entity(r) for r in rows], total

    async def get_by_id(self, team_id: UUID, organization_id: UUID) -> TeamDetail | None:
        result = await self._session.execute(
            text("""
                SELECT t.id, t.name, t.manager_id, t.organization_id, t.created_at, t.updated_at,
                       u.first_name || ' ' || u.last_name AS manager_name,
                       COUNT(m.id) FILTER (WHERE m.deleted_at IS NULL) AS member_count
                FROM teams t
                LEFT JOIN users u ON t.manager_id = u.id AND u.deleted_at IS NULL
                LEFT JOIN users m ON m.team_id = t.id
                WHERE t.id = :id AND t.organization_id = :org_id AND t.deleted_at IS NULL
                GROUP BY t.id, t.name, t.manager_id, t.organization_id, t.created_at, t.updated_at,
                         u.first_name, u.last_name
            """),
            {"id": team_id, "org_id": organization_id},
        )
        row = result.one_or_none()
        return self._to_entity(row) if row else None

    async def name_exists(self, name: str, organization_id: UUID, exclude_id: UUID | None = None) -> bool:
        sql = "SELECT 1 FROM teams WHERE name = :name AND organization_id = :org_id AND deleted_at IS NULL"
        params: dict = {"name": name, "org_id": organization_id}
        if exclude_id:
            sql += " AND id != :exclude_id"
            params["exclude_id"] = exclude_id
        result = await self._session.execute(text(sql), params)
        return result.one_or_none() is not None

    async def manager_valid(self, manager_id: UUID, organization_id: UUID) -> bool:
        result = await self._session.execute(
            text("""
                SELECT 1 FROM users
                WHERE id = :id AND organization_id = :org_id
                  AND role IN ('manager', 'administrator')
                  AND deleted_at IS NULL
            """),
            {"id": manager_id, "org_id": organization_id},
        )
        return result.one_or_none() is not None

    async def create(self, organization_id: UUID, name: str, manager_id: UUID | None) -> TeamDetail:
        new_id = uuid4()
        await self._session.execute(
            text("""
                INSERT INTO teams (id, organization_id, manager_id, name)
                VALUES (:id, :org_id, :manager_id, :name)
            """),
            {"id": new_id, "org_id": organization_id, "manager_id": manager_id, "name": name},
        )
        await self._session.flush()
        return await self.get_by_id(new_id, organization_id)  # type: ignore[return-value]

    async def update(
        self, team_id: UUID, organization_id: UUID, name: str | None, manager_id: UUID | None
    ) -> TeamDetail | None:
        await self._session.execute(
            text("""
                UPDATE teams SET
                    name       = COALESCE(:name, name),
                    manager_id = COALESCE(CAST(:manager_id AS uuid), manager_id),
                    updated_at = now()
                WHERE id = :id AND organization_id = :org_id AND deleted_at IS NULL
            """),
            {"id": team_id, "org_id": organization_id, "name": name, "manager_id": manager_id},
        )
        await self._session.flush()
        return await self.get_by_id(team_id, organization_id)

    async def get_members(self, team_id: UUID, organization_id: UUID) -> list[TeamMemberDetail]:
        result = await self._session.execute(
            text("""
                SELECT id, first_name, last_name, role, status
                FROM users
                WHERE team_id = :team_id AND organization_id = :org_id AND deleted_at IS NULL
                ORDER BY first_name, last_name
            """),
            {"team_id": team_id, "org_id": organization_id},
        )
        return [
            TeamMemberDetail(id=r.id, first_name=r.first_name, last_name=r.last_name, role=r.role, status=r.status)
            for r in result.fetchall()
        ]

    async def add_member(self, team_id: UUID, user_id: UUID, organization_id: UUID) -> bool:
        result = await self._session.execute(
            text("""
                UPDATE users SET team_id = :team_id, updated_at = now()
                WHERE id = :user_id AND organization_id = :org_id AND deleted_at IS NULL
            """),
            {"team_id": team_id, "user_id": user_id, "org_id": organization_id},
        )
        await self._session.flush()
        return result.rowcount > 0

    async def remove_member(self, team_id: UUID, user_id: UUID, organization_id: UUID) -> bool:
        result = await self._session.execute(
            text("""
                UPDATE users SET team_id = NULL, updated_at = now()
                WHERE id = :user_id AND team_id = :team_id AND organization_id = :org_id AND deleted_at IS NULL
            """),
            {"user_id": user_id, "team_id": team_id, "org_id": organization_id},
        )
        await self._session.flush()
        return result.rowcount > 0

    async def user_exists(self, user_id: UUID, organization_id: UUID) -> bool:
        result = await self._session.execute(
            text("SELECT 1 FROM users WHERE id = :id AND organization_id = :org_id AND deleted_at IS NULL"),
            {"id": user_id, "org_id": organization_id},
        )
        return result.one_or_none() is not None

    @staticmethod
    def _to_entity(row) -> TeamDetail:
        return TeamDetail(
            id=row.id,
            organization_id=row.organization_id,
            name=row.name,
            manager_id=row.manager_id,
            manager_name=row.manager_name,
            member_count=int(row.member_count),
            created_at=row.created_at,
            updated_at=row.updated_at,
        )
