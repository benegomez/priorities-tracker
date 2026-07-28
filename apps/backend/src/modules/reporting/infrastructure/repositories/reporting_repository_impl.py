from uuid import UUID

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession


class ReportingRepositoryImpl:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_individual_report(self, employee_id: UUID, organization_id: UUID, weeks: int):
        """Returns weekly breakdown of priorities for an employee."""
        result = await self._session.execute(
            text("""
                SELECT
                    p.week_start,
                    COUNT(*) AS committed,
                    COUNT(*) FILTER (WHERE p.status = 'completed') AS completed,
                    COUNT(*) FILTER (WHERE p.status = 'carried_over') AS carried_over
                FROM priorities p
                WHERE p.owner_id = :employee_id
                  AND p.organization_id = :org_id
                  AND p.deleted_at IS NULL
                  AND p.week_start >= CURRENT_DATE - (:weeks * INTERVAL '7 days')
                GROUP BY p.week_start
                ORDER BY p.week_start DESC
            """),
            {"employee_id": employee_id, "org_id": organization_id, "weeks": weeks},
        )
        return result.fetchall()

    async def get_employee_info(self, employee_id: UUID, organization_id: UUID):
        result = await self._session.execute(
            text("""
                SELECT id, first_name, last_name
                FROM users
                WHERE id = :employee_id AND organization_id = :org_id AND deleted_at IS NULL
            """),
            {"employee_id": employee_id, "org_id": organization_id},
        )
        return result.one_or_none()

    async def get_latest_crs(self, employee_id: UUID, organization_id: UUID):
        result = await self._session.execute(
            text("""
                SELECT score, trend FROM crs_scores
                WHERE employee_id = :employee_id AND organization_id = :org_id AND deleted_at IS NULL
                ORDER BY week_start DESC LIMIT 1
            """),
            {"employee_id": employee_id, "org_id": organization_id},
        )
        return result.one_or_none()

    async def get_crs_by_week(self, employee_id: UUID, organization_id: UUID, weeks: int):
        result = await self._session.execute(
            text("""
                SELECT week_start, score FROM crs_scores
                WHERE employee_id = :employee_id AND organization_id = :org_id AND deleted_at IS NULL
                  AND week_start >= CURRENT_DATE - (:weeks * INTERVAL '7 days')
                ORDER BY week_start DESC
            """),
            {"employee_id": employee_id, "org_id": organization_id, "weeks": weeks},
        )
        return {row.week_start: float(row.score) for row in result.fetchall()}

    async def get_direct_reports(self, manager_id: UUID, organization_id: UUID):
        result = await self._session.execute(
            text("""
                SELECT id, first_name, last_name
                FROM users
                WHERE manager_id = :manager_id AND organization_id = :org_id AND deleted_at IS NULL
            """),
            {"manager_id": manager_id, "org_id": organization_id},
        )
        return result.fetchall()

    async def get_member_completion_rate(self, employee_id: UUID, organization_id: UUID, weeks: int) -> float:
        result = await self._session.execute(
            text("""
                SELECT
                    COUNT(*) AS total,
                    COUNT(*) FILTER (WHERE status = 'completed') AS completed
                FROM priorities
                WHERE owner_id = :employee_id AND organization_id = :org_id AND deleted_at IS NULL
                  AND week_start >= CURRENT_DATE - (:weeks * INTERVAL '7 days')
            """),
            {"employee_id": employee_id, "org_id": organization_id, "weeks": weeks},
        )
        row = result.one()
        if not row.total:
            return 0.0
        return round(row.completed / row.total * 100, 1)

    async def get_team_weekly_breakdown(self, member_ids: list[UUID], organization_id: UUID, weeks: int):
        if not member_ids:
            return []
        result = await self._session.execute(
            text("""
                SELECT
                    ci.week_start,
                    COUNT(DISTINCT ci.id) FILTER (WHERE ci.status = 'submitted') AS checkins_submitted,
                    COUNT(DISTINCT co.id) FILTER (WHERE co.status = 'submitted') AS checkouts_submitted,
                    COUNT(p.id) AS total_priorities,
                    COUNT(p.id) FILTER (WHERE p.status = 'completed') AS completed_priorities
                FROM check_ins ci
                LEFT JOIN check_outs co ON co.checkin_id = ci.id AND co.deleted_at IS NULL
                LEFT JOIN priorities p ON p.checkin_id = ci.id AND p.deleted_at IS NULL
                WHERE ci.employee_id = ANY(:member_ids)
                  AND ci.organization_id = :org_id
                  AND ci.deleted_at IS NULL
                  AND ci.week_start >= CURRENT_DATE - (:weeks * INTERVAL '7 days')
                GROUP BY ci.week_start
                ORDER BY ci.week_start DESC
            """),
            {"member_ids": member_ids, "org_id": organization_id, "weeks": weeks},
        )
        return result.fetchall()

    async def get_project(self, project_id: UUID, organization_id: UUID):
        result = await self._session.execute(
            text("""
                SELECT id, name, status FROM projects
                WHERE id = :project_id AND organization_id = :org_id AND deleted_at IS NULL
            """),
            {"project_id": project_id, "org_id": organization_id},
        )
        return result.one_or_none()

    async def get_project_phases_report(self, project_id: UUID, organization_id: UUID, weeks: int):
        result = await self._session.execute(
            text("""
                SELECT
                    ph.id,
                    ph.name,
                    COUNT(p.id) AS total_priorities,
                    COUNT(p.id) FILTER (WHERE p.status = 'completed') AS completed_priorities
                FROM project_phases ph
                LEFT JOIN priorities p ON p.phase_id = ph.id
                    AND p.deleted_at IS NULL
                    AND p.week_start >= CURRENT_DATE - (:weeks * INTERVAL '7 days')
                WHERE ph.project_id = :project_id
                  AND ph.organization_id = :org_id
                  AND ph.deleted_at IS NULL
                GROUP BY ph.id, ph.name
                ORDER BY ph.created_at
            """),
            {"project_id": project_id, "org_id": organization_id, "weeks": weeks},
        )
        return result.fetchall()
