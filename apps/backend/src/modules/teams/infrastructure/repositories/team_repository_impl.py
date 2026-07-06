from datetime import date
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession


class TeamRepositoryImpl:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_direct_reports(self, manager_id: UUID, organization_id: UUID) -> list:
        result = await self._session.execute(
            text("""
                SELECT id, first_name, last_name, email
                FROM users
                WHERE manager_id = :manager_id
                  AND organization_id = :org_id
                  AND status = 'active'
                  AND deleted_at IS NULL
                ORDER BY first_name, last_name
            """),
            {"manager_id": manager_id, "org_id": organization_id},
        )
        return result.fetchall()

    async def get_latest_crs_batch(self, employee_ids: list[UUID], organization_id: UUID) -> dict[UUID, any]:
        if not employee_ids:
            return {}
        result = await self._session.execute(
            text("""
                SELECT DISTINCT ON (employee_id) employee_id, score, trend, risk_level
                FROM crs_scores
                WHERE employee_id = ANY(:ids)
                  AND organization_id = :org_id
                  AND deleted_at IS NULL
                ORDER BY employee_id, week_start DESC
            """),
            {"ids": employee_ids, "org_id": organization_id},
        )
        return {row.employee_id: row for row in result.fetchall()}

    async def get_week_checkins_batch(self, employee_ids: list[UUID], organization_id: UUID, week_start: date) -> dict[UUID, str]:
        if not employee_ids:
            return {}
        result = await self._session.execute(
            text("""
                SELECT employee_id, status
                FROM check_ins
                WHERE employee_id = ANY(:ids)
                  AND organization_id = :org_id
                  AND week_start = :week_start
                  AND deleted_at IS NULL
            """),
            {"ids": employee_ids, "org_id": organization_id, "week_start": week_start},
        )
        return {row.employee_id: row.status for row in result.fetchall()}

    async def get_week_checkouts_batch(self, employee_ids: list[UUID], organization_id: UUID, week_start: date) -> dict[UUID, str]:
        if not employee_ids:
            return {}
        result = await self._session.execute(
            text("""
                SELECT employee_id, status
                FROM check_outs
                WHERE employee_id = ANY(:ids)
                  AND organization_id = :org_id
                  AND week_start = :week_start
                  AND deleted_at IS NULL
            """),
            {"ids": employee_ids, "org_id": organization_id, "week_start": week_start},
        )
        return {row.employee_id: row.status for row in result.fetchall()}

    async def validate_direct_report(self, employee_id: UUID, manager_id: UUID, organization_id: UUID):
        """Returns user row if valid direct report, raises 403 otherwise."""
        result = await self._session.execute(
            text("""
                SELECT id, first_name, last_name FROM users
                WHERE id = :employee_id
                  AND manager_id = :manager_id
                  AND organization_id = :org_id
                  AND deleted_at IS NULL
            """),
            {"employee_id": employee_id, "manager_id": manager_id, "org_id": organization_id},
        )
        row = result.one_or_none()
        if not row:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Employee is not a direct report")
        return row

    async def get_checkin_for_employee(self, employee_id: UUID, organization_id: UUID, week_start: date):
        result = await self._session.execute(
            text("""
                SELECT id, employee_id, organization_id, week_start, status, submitted_at, created_at, updated_at
                FROM check_ins
                WHERE employee_id = :employee_id
                  AND organization_id = :org_id
                  AND week_start = :week_start
                  AND deleted_at IS NULL
            """),
            {"employee_id": employee_id, "org_id": organization_id, "week_start": week_start},
        )
        return result.one_or_none()

    async def load_priorities_with_tasks(self, checkin_id: UUID, organization_id: UUID) -> list:
        result = await self._session.execute(
            text("""
                SELECT pr.id, pr.title, pr.description, pr.priority_level, pr.status,
                       pp.name as phase_name, p.name as project_name
                FROM priorities pr
                LEFT JOIN project_phases pp ON pr.phase_id = pp.id
                LEFT JOIN projects p ON pp.project_id = p.id
                WHERE pr.checkin_id = :checkin_id AND pr.organization_id = :org_id AND pr.deleted_at IS NULL
                ORDER BY pr.created_at
            """),
            {"checkin_id": checkin_id, "org_id": organization_id},
        )
        priorities = result.fetchall()

        priority_ids = [p.id for p in priorities]
        tasks_by_priority: dict[UUID, list] = {pid: [] for pid in priority_ids}

        if priority_ids:
            task_result = await self._session.execute(
                text("""
                    SELECT id, priority_id, title, status
                    FROM tasks
                    WHERE priority_id = ANY(:priority_ids) AND organization_id = :org_id AND deleted_at IS NULL
                    ORDER BY created_at
                """),
                {"priority_ids": priority_ids, "org_id": organization_id},
            )
            for t in task_result.fetchall():
                tasks_by_priority[t.priority_id].append({"id": t.id, "title": t.title, "status": t.status})

        return [
            {
                "id": p.id, "title": p.title, "description": p.description,
                "priority_level": p.priority_level, "status": p.status,
                "phase_name": p.phase_name, "project_name": p.project_name,
                "tasks": tasks_by_priority.get(p.id, []),
            }
            for p in priorities
        ]
