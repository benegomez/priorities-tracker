from uuid import UUID

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from src.modules.priorities.domain.entities.priority import Priority
from src.modules.priorities.domain.repositories.priority_repository import PriorityRepository


class PriorityRepositoryImpl(PriorityRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def save(self, priority: Priority) -> None:
        query = text("""
            INSERT INTO priorities (id, organization_id, checkin_id, phase_id, owner_id, week_start,
                                    title, description, priority_level, status)
            VALUES (:id, :organization_id, :checkin_id, :phase_id, :owner_id, :week_start,
                    :title, :description, :priority_level, :status)
        """)
        await self._session.execute(query, {
            "id": priority.id,
            "organization_id": priority.organization_id,
            "checkin_id": priority.checkin_id,
            "phase_id": priority.phase_id,
            "owner_id": priority.owner_id,
            "week_start": priority.week_start,
            "title": priority.title,
            "description": priority.description,
            "priority_level": priority.priority_level,
            "status": priority.status,
        })
        await self._session.commit()

    async def get_by_id(self, priority_id: UUID, organization_id: UUID) -> Priority | None:
        query = text("""
            SELECT id, organization_id, checkin_id, phase_id, owner_id, week_start,
                   title, description, priority_level, status, created_at, updated_at
            FROM priorities
            WHERE id = :id AND organization_id = :organization_id AND deleted_at IS NULL
        """)
        result = await self._session.execute(query, {"id": priority_id, "organization_id": organization_id})
        row = result.one_or_none()
        return self._to_entity(row) if row else None

    async def count_by_checkin(self, checkin_id: UUID, organization_id: UUID) -> int:
        query = text("""
            SELECT count(*) FROM priorities
            WHERE checkin_id = :checkin_id AND organization_id = :organization_id AND deleted_at IS NULL
        """)
        result = await self._session.execute(query, {"checkin_id": checkin_id, "organization_id": organization_id})
        return result.scalar_one()

    async def transition_to_planned(self, checkin_id: UUID, organization_id: UUID) -> None:
        query = text("""
            UPDATE priorities SET status = 'planned', updated_at = now()
            WHERE checkin_id = :checkin_id AND organization_id = :organization_id
              AND status = 'draft' AND deleted_at IS NULL
        """)
        await self._session.execute(query, {"checkin_id": checkin_id, "organization_id": organization_id})

    @staticmethod
    def _to_entity(row) -> Priority:
        return Priority(
            id=row.id,
            organization_id=row.organization_id,
            checkin_id=row.checkin_id,
            phase_id=row.phase_id,
            owner_id=row.owner_id,
            week_start=row.week_start,
            title=row.title,
            description=row.description,
            priority_level=row.priority_level,
            status=row.status,
            created_at=row.created_at,
            updated_at=row.updated_at,
        )
