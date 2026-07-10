from dataclasses import dataclass
from datetime import date, datetime, timezone
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from src.modules.ai_insights.infrastructure.ai_summary_repository import AISummaryRepository
from src.modules.ai_insights.infrastructure.openai_client import OpenAIClient
from src.modules.teams.infrastructure.repositories.team_repository_impl import TeamRepositoryImpl


SYSTEM_PROMPT = """Eres un asistente de gestión de equipos. Tu rol es generar resúmenes ejecutivos semanales para managers.
Responde siempre en español. Sé conciso (máximo 200 palabras). Estructura tu respuesta en:
1. Resumen general (1-2 oraciones)
2. Logros destacados
3. Puntos de atención
4. Recomendaciones (si aplica)
No inventes datos. Solo usa la información proporcionada."""


@dataclass
class TeamSummaryResult:
    summary: str
    generated_at: datetime
    model: str | None
    data_snapshot: dict
    fallback: bool
    cached: bool


class GenerateTeamSummaryUseCase:
    def __init__(self, session: AsyncSession, openai_client: OpenAIClient) -> None:
        self._session = session
        self._openai = openai_client
        self._team_repo = TeamRepositoryImpl(session)
        self._summary_repo = AISummaryRepository(session)

    async def execute(self, manager_id: UUID, organization_id: UUID, regenerate: bool = False) -> TeamSummaryResult:
        week_start = date.today()

        # Check cache
        if not regenerate:
            cached = await self._summary_repo.get_cached(manager_id, week_start, organization_id)
            if cached:
                return TeamSummaryResult(
                    summary=cached["summary"],
                    generated_at=cached["generated_at"],
                    model=cached["model"],
                    data_snapshot=cached["data_snapshot"],
                    fallback=cached["fallback"],
                    cached=True,
                )

        # Delete existing cache if regenerating
        if regenerate:
            await self._summary_repo.delete(manager_id, week_start, organization_id)

        # Get team data
        members = await self._team_repo.get_direct_reports(manager_id, organization_id)
        if not members:
            return TeamSummaryResult(
                summary="No tienes miembros en tu equipo.",
                generated_at=datetime.now(timezone.utc),
                model=None,
                data_snapshot={"team_size": 0, "week_start": str(week_start), "avg_crs": 0, "total_priorities": 0, "completed_priorities": 0, "completion_rate": 0},
                fallback=True,
                cached=False,
            )

        member_ids = [m.id for m in members]
        crs_batch = await self._team_repo.get_latest_crs_batch(member_ids, organization_id)

        # Get priorities/tasks counts from CRS scores (need extended query)
        crs_extended = await self._get_crs_with_counts(member_ids, organization_id)

        # Build member data and snapshot
        members_data = []
        total_priorities = 0
        completed_priorities = 0
        total_tasks = 0
        completed_tasks = 0
        crs_scores = []

        for m in members:
            crs = crs_batch.get(m.id)
            ext = crs_extended.get(m.id, {})
            md = {
                "name": f"{m.first_name} {m.last_name}",
                "score": crs.score if crs else 0,
                "trend": crs.trend if crs else "stable",
                "risk_level": crs.risk_level if crs else "low",
                "priorities_total": ext.get("priorities_total", 0),
                "priorities_completed": ext.get("priorities_completed", 0),
                "tasks_total": ext.get("tasks_total", 0),
                "tasks_completed": ext.get("tasks_completed", 0),
            }
            members_data.append(md)
            total_priorities += md["priorities_total"]
            completed_priorities += md["priorities_completed"]
            total_tasks += md["tasks_total"]
            completed_tasks += md["tasks_completed"]
            if crs:
                crs_scores.append(float(crs.score))

        avg_crs = round(float(sum(crs_scores) / len(crs_scores)), 1) if crs_scores else 0.0
        completion_rate = round(float(completed_priorities / total_priorities * 100), 1) if total_priorities > 0 else 0.0

        data_snapshot = {
            "team_size": len(members),
            "week_start": str(week_start),
            "avg_crs": avg_crs,
            "total_priorities": int(total_priorities),
            "completed_priorities": int(completed_priorities),
            "completion_rate": completion_rate,
        }

        # Build prompt
        user_prompt = self._build_user_prompt(week_start, members_data, data_snapshot)

        # Call OpenAI
        ai_response = await self._openai.generate(SYSTEM_PROMPT, user_prompt)

        now = datetime.now(timezone.utc)

        if ai_response:
            # Persist in cache
            await self._summary_repo.save(
                manager_id=manager_id,
                week_start=week_start,
                organization_id=organization_id,
                summary=ai_response,
                model=self._openai.model_name,
                data_snapshot=data_snapshot,
            )
            return TeamSummaryResult(
                summary=ai_response,
                generated_at=now,
                model=self._openai.model_name,
                data_snapshot=data_snapshot,
                fallback=False,
                cached=False,
            )

        # Fallback (not cached)
        fallback_summary = self._build_fallback_summary(data_snapshot, members_data)
        return TeamSummaryResult(
            summary=fallback_summary,
            generated_at=now,
            model=None,
            data_snapshot=data_snapshot,
            fallback=True,
            cached=False,
        )

    async def _get_crs_with_counts(self, employee_ids: list[UUID], organization_id: UUID) -> dict[UUID, dict]:
        """Get latest CRS with priority/task counts."""
        from sqlalchemy import text
        result = await self._session.execute(
            text("""
                SELECT DISTINCT ON (employee_id)
                    employee_id, priorities_total, priorities_completed, tasks_total, tasks_completed
                FROM crs_scores
                WHERE employee_id = ANY(:ids)
                  AND organization_id = :org_id
                  AND deleted_at IS NULL
                ORDER BY employee_id, week_start DESC
            """),
            {"ids": employee_ids, "org_id": organization_id},
        )
        return {
            row.employee_id: {
                "priorities_total": row.priorities_total,
                "priorities_completed": row.priorities_completed,
                "tasks_total": row.tasks_total,
                "tasks_completed": row.tasks_completed,
            }
            for row in result.fetchall()
        }

    def _build_user_prompt(self, week_start: date, members_data: list[dict], snapshot: dict) -> str:
        member_lines = []
        for m in members_data:
            member_lines.append(
                f"- {m['name']}: CRS {m['score']:.1f} ({m['trend']}), "
                f"{m['priorities_completed']}/{m['priorities_total']} prioridades completadas, "
                f"{m['tasks_completed']}/{m['tasks_total']} tareas"
            )

        high_risk = sum(1 for m in members_data if m["risk_level"] == "high")
        declining = sum(1 for m in members_data if m["trend"] == "declining")

        return f"""Genera un resumen ejecutivo semanal para el equipo con los siguientes datos:

Semana: {week_start}
Tamaño del equipo: {snapshot['team_size']} personas

Datos por miembro:
{chr(10).join(member_lines)}

Métricas agregadas:
- CRS promedio: {snapshot['avg_crs']}
- Tasa de cumplimiento: {snapshot['completion_rate']}%
- Miembros en riesgo alto: {high_risk}
- Miembros con tendencia declining: {declining}"""

    def _build_fallback_summary(self, snapshot: dict, members_data: list[dict]) -> str:
        declining = [m for m in members_data if m["trend"] == "declining"]
        high_risk = [m for m in members_data if m["risk_level"] == "high"]

        parts = [
            f"Resumen automático: El equipo completó {snapshot['completed_priorities']} de {snapshot['total_priorities']} prioridades ({snapshot['completion_rate']:.0f}%).",
            f"CRS promedio: {snapshot['avg_crs']:.1f}.",
        ]
        if declining:
            parts.append(f"{len(declining)} miembro(s) con tendencia declining.")
        if high_risk:
            parts.append(f"{len(high_risk)} miembro(s) en riesgo alto.")

        return " ".join(parts)
