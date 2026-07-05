from uuid import UUID

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession


class ProjectRepositoryImpl:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_by_org(self, organization_id: UUID, status_filter: str | None = None, page: int = 1, page_size: int = 20):
        where = "p.organization_id = :org_id AND p.deleted_at IS NULL"
        params: dict = {"org_id": organization_id}
        if status_filter:
            where += " AND p.status = :status"
            params["status"] = status_filter

        count_result = await self._session.execute(text(f"SELECT count(*) FROM projects p WHERE {where}"), params)
        total = count_result.scalar_one()

        result = await self._session.execute(
            text(f"""
                SELECT p.id, p.name, p.description, p.status, p.owner_id,
                       u.first_name || ' ' || u.last_name as owner_name,
                       (SELECT count(*) FROM project_phases pp WHERE pp.project_id = p.id AND pp.deleted_at IS NULL) as phases_count,
                       (SELECT count(*) FROM project_members pm WHERE pm.project_id = p.id AND pm.deleted_at IS NULL) as members_count,
                       p.created_at
                FROM projects p
                LEFT JOIN users u ON p.owner_id = u.id
                WHERE {where}
                ORDER BY p.created_at DESC
                LIMIT :limit OFFSET :offset
            """),
            {**params, "limit": page_size, "offset": (page - 1) * page_size},
        )
        return result.fetchall(), total

    async def get_by_id(self, project_id: UUID, organization_id: UUID):
        result = await self._session.execute(
            text("""
                SELECT p.id, p.name, p.description, p.status, p.owner_id,
                       u.first_name || ' ' || u.last_name as owner_name,
                       p.created_at, p.updated_at
                FROM projects p
                LEFT JOIN users u ON p.owner_id = u.id
                WHERE p.id = :id AND p.organization_id = :org_id AND p.deleted_at IS NULL
            """),
            {"id": project_id, "org_id": organization_id},
        )
        return result.one_or_none()

    async def get_phases(self, project_id: UUID, organization_id: UUID):
        result = await self._session.execute(
            text("""
                SELECT id, name, status FROM project_phases
                WHERE project_id = :project_id AND organization_id = :org_id AND deleted_at IS NULL
                ORDER BY created_at
            """),
            {"project_id": project_id, "org_id": organization_id},
        )
        return result.fetchall()

    async def get_members(self, project_id: UUID, organization_id: UUID):
        result = await self._session.execute(
            text("""
                SELECT pm.user_id, u.first_name || ' ' || u.last_name as full_name, u.role
                FROM project_members pm
                JOIN users u ON pm.user_id = u.id
                WHERE pm.project_id = :project_id AND pm.organization_id = :org_id AND pm.deleted_at IS NULL
                ORDER BY u.first_name
            """),
            {"project_id": project_id, "org_id": organization_id},
        )
        return result.fetchall()

    async def save_project(self, project_id: UUID, organization_id: UUID, owner_id: UUID | None, name: str, description: str | None):
        await self._session.execute(
            text("""
                INSERT INTO projects (id, organization_id, owner_id, name, description, status)
                VALUES (:id, :org_id, :owner_id, :name, :description, 'draft')
            """),
            {"id": project_id, "org_id": organization_id, "owner_id": owner_id, "name": name, "description": description},
        )
        await self._session.commit()

    async def update_project(self, project_id: UUID, organization_id: UUID, **fields):
        sets = ", ".join(f"{k} = :{k}" for k in fields)
        sets += ", updated_at = now()"
        await self._session.execute(
            text(f"UPDATE projects SET {sets} WHERE id = :id AND organization_id = :org_id AND deleted_at IS NULL"),
            {"id": project_id, "org_id": organization_id, **fields},
        )
        await self._session.commit()

    async def save_phase(self, phase_id: UUID, organization_id: UUID, project_id: UUID, name: str):
        await self._session.execute(
            text("""
                INSERT INTO project_phases (id, organization_id, project_id, name, status)
                VALUES (:id, :org_id, :project_id, :name, 'planned')
            """),
            {"id": phase_id, "org_id": organization_id, "project_id": project_id, "name": name},
        )
        await self._session.commit()

    async def update_phase(self, phase_id: UUID, organization_id: UUID, **fields):
        sets = ", ".join(f"{k} = :{k}" for k in fields)
        sets += ", updated_at = now()"
        await self._session.execute(
            text(f"UPDATE project_phases SET {sets} WHERE id = :id AND organization_id = :org_id AND deleted_at IS NULL"),
            {"id": phase_id, "org_id": organization_id, **fields},
        )
        await self._session.commit()

    async def get_phase(self, phase_id: UUID, organization_id: UUID):
        result = await self._session.execute(
            text("SELECT id, project_id, name, status FROM project_phases WHERE id = :id AND organization_id = :org_id AND deleted_at IS NULL"),
            {"id": phase_id, "org_id": organization_id},
        )
        return result.one_or_none()

    async def add_member(self, member_id: UUID, organization_id: UUID, project_id: UUID, user_id: UUID):
        await self._session.execute(
            text("""
                INSERT INTO project_members (id, organization_id, project_id, user_id)
                VALUES (:id, :org_id, :project_id, :user_id)
            """),
            {"id": member_id, "org_id": organization_id, "project_id": project_id, "user_id": user_id},
        )
        await self._session.commit()

    async def remove_member(self, organization_id: UUID, project_id: UUID, user_id: UUID):
        await self._session.execute(
            text("""
                UPDATE project_members SET deleted_at = now()
                WHERE project_id = :project_id AND user_id = :user_id
                  AND organization_id = :org_id AND deleted_at IS NULL
            """),
            {"project_id": project_id, "user_id": user_id, "org_id": organization_id},
        )
        await self._session.commit()

    async def member_exists(self, organization_id: UUID, project_id: UUID, user_id: UUID) -> bool:
        result = await self._session.execute(
            text("""
                SELECT 1 FROM project_members
                WHERE project_id = :project_id AND user_id = :user_id
                  AND organization_id = :org_id AND deleted_at IS NULL
            """),
            {"project_id": project_id, "user_id": user_id, "org_id": organization_id},
        )
        return result.one_or_none() is not None

    async def user_belongs_to_org(self, user_id: UUID, organization_id: UUID) -> bool:
        result = await self._session.execute(
            text("SELECT 1 FROM users WHERE id = :id AND organization_id = :org_id AND deleted_at IS NULL"),
            {"id": user_id, "org_id": organization_id},
        )
        return result.one_or_none() is not None

    async def get_available_phases(self, organization_id: UUID):
        result = await self._session.execute(
            text("""
                SELECT pp.id, pp.name, p.name as project_name
                FROM project_phases pp
                JOIN projects p ON pp.project_id = p.id
                WHERE pp.organization_id = :org_id
                  AND pp.status = 'active' AND p.status = 'active'
                  AND pp.deleted_at IS NULL AND p.deleted_at IS NULL
                ORDER BY p.name, pp.name
            """),
            {"org_id": organization_id},
        )
        return result.fetchall()
