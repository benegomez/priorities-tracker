from datetime import date
from uuid import UUID

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession


class CRSRepositoryImpl:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_latest_by_employee(self, employee_id: UUID, organization_id: UUID):
        result = await self._session.execute(
            text("""
                SELECT id, employee_id, organization_id, checkout_id, week_start, score,
                       trend, risk_level, formula_version, priorities_total, priorities_completed,
                       tasks_total, tasks_completed, created_at
                FROM crs_scores
                WHERE employee_id = :employee_id AND organization_id = :org_id AND deleted_at IS NULL
                ORDER BY week_start DESC
                LIMIT 1
            """),
            {"employee_id": employee_id, "org_id": organization_id},
        )
        return result.one_or_none()

    async def get_history(self, employee_id: UUID, organization_id: UUID, weeks: int = 8):
        result = await self._session.execute(
            text("""
                SELECT week_start, score, trend, risk_level
                FROM crs_scores
                WHERE employee_id = :employee_id AND organization_id = :org_id AND deleted_at IS NULL
                ORDER BY week_start DESC
                LIMIT :weeks
            """),
            {"employee_id": employee_id, "org_id": organization_id, "weeks": weeks},
        )
        return result.fetchall()

    async def get_last_n_scores(self, employee_id: UUID, organization_id: UUID, n: int = 4) -> list[float]:
        result = await self._session.execute(
            text("""
                SELECT score FROM crs_scores
                WHERE employee_id = :employee_id AND organization_id = :org_id AND deleted_at IS NULL
                ORDER BY week_start DESC
                LIMIT :n
            """),
            {"employee_id": employee_id, "org_id": organization_id, "n": n},
        )
        return [float(row.score) for row in result.fetchall()]

    async def save(self, crs_id: UUID, organization_id: UUID, employee_id: UUID, checkout_id: UUID,
                   week_start: date, score: float, trend: str, risk_level: str,
                   formula_version: str, priorities_total: int, priorities_completed: int,
                   tasks_total: int, tasks_completed: int) -> None:
        await self._session.execute(
            text("""
                INSERT INTO crs_scores (id, organization_id, employee_id, checkout_id, week_start,
                    score, trend, risk_level, formula_version,
                    priorities_total, priorities_completed, tasks_total, tasks_completed)
                VALUES (:id, :org_id, :employee_id, :checkout_id, :week_start,
                    :score, :trend, :risk_level, :formula_version,
                    :priorities_total, :priorities_completed, :tasks_total, :tasks_completed)
            """),
            {
                "id": crs_id, "org_id": organization_id, "employee_id": employee_id,
                "checkout_id": checkout_id, "week_start": week_start,
                "score": score, "trend": trend, "risk_level": risk_level,
                "formula_version": formula_version,
                "priorities_total": priorities_total, "priorities_completed": priorities_completed,
                "tasks_total": tasks_total, "tasks_completed": tasks_completed,
            },
        )
        await self._session.commit()
