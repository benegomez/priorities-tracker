import json
from datetime import date
from uuid import UUID

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession


class AISummaryRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_cached(self, manager_id: UUID, week_start: date, organization_id: UUID) -> dict | None:
        result = await self._session.execute(
            text("""
                SELECT summary, model, data_snapshot, fallback, created_at
                FROM ai_summaries
                WHERE manager_id = :mgr AND week_start = :ws AND organization_id = :org
            """),
            {"mgr": manager_id, "ws": week_start, "org": organization_id},
        )
        row = result.first()
        if row is None:
            return None
        return {
            "summary": row.summary,
            "model": row.model,
            "data_snapshot": row.data_snapshot if isinstance(row.data_snapshot, dict) else json.loads(row.data_snapshot),
            "fallback": row.fallback,
            "generated_at": row.created_at,
        }

    async def save(
        self,
        manager_id: UUID,
        week_start: date,
        organization_id: UUID,
        summary: str,
        model: str | None,
        data_snapshot: dict,
    ) -> None:
        snapshot_json = json.dumps(data_snapshot)
        await self._session.execute(
            text("""
                INSERT INTO ai_summaries (id, organization_id, manager_id, week_start, summary, model, data_snapshot, fallback)
                VALUES (gen_random_uuid(), :org, :mgr, :ws, :summary, :model, CAST(:snapshot AS jsonb), false)
                ON CONFLICT (manager_id, week_start, organization_id)
                DO UPDATE SET summary = :summary, model = :model, data_snapshot = CAST(:snapshot AS jsonb), created_at = now()
            """),
            {
                "org": organization_id,
                "mgr": manager_id,
                "ws": week_start,
                "summary": summary,
                "model": model,
                "snapshot": snapshot_json,
            },
        )
        await self._session.commit()

    async def delete(self, manager_id: UUID, week_start: date, organization_id: UUID) -> None:
        await self._session.execute(
            text("""
                DELETE FROM ai_summaries
                WHERE manager_id = :mgr AND week_start = :ws AND organization_id = :org
            """),
            {"mgr": manager_id, "ws": week_start, "org": organization_id},
        )
        await self._session.commit()
