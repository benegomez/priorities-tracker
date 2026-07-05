from datetime import date
from uuid import UUID, uuid4

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from src.modules.checkin.domain.entities.checkin import WeeklyCheckIn
from src.modules.checkin.domain.repositories.checkin_repository import CheckInRepository


class CheckInRepositoryImpl(CheckInRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def save(self, checkin: WeeklyCheckIn) -> None:
        query = text("""
            INSERT INTO check_ins (id, organization_id, employee_id, week_start, status, submitted_at)
            VALUES (:id, :organization_id, :employee_id, :week_start, :status, :submitted_at)
        """)
        await self._session.execute(query, {
            "id": checkin.id,
            "organization_id": checkin.organization_id,
            "employee_id": checkin.employee_id,
            "week_start": checkin.week_start,
            "status": checkin.status,
            "submitted_at": checkin.submitted_at,
        })
        await self._session.commit()

    async def get_by_id(self, checkin_id: UUID, organization_id: UUID) -> WeeklyCheckIn | None:
        query = text("""
            SELECT id, organization_id, employee_id, week_start, status, submitted_at, created_at, updated_at
            FROM check_ins
            WHERE id = :id AND organization_id = :organization_id AND deleted_at IS NULL
        """)
        result = await self._session.execute(query, {"id": checkin_id, "organization_id": organization_id})
        row = result.one_or_none()
        return self._to_entity(row) if row else None

    async def get_by_employee_and_week(
        self, employee_id: UUID, week_start: date, organization_id: UUID
    ) -> WeeklyCheckIn | None:
        query = text("""
            SELECT id, organization_id, employee_id, week_start, status, submitted_at, created_at, updated_at
            FROM check_ins
            WHERE employee_id = :employee_id AND week_start = :week_start
              AND organization_id = :organization_id AND deleted_at IS NULL
        """)
        result = await self._session.execute(query, {
            "employee_id": employee_id,
            "week_start": week_start,
            "organization_id": organization_id,
        })
        row = result.one_or_none()
        return self._to_entity(row) if row else None

    async def update(self, checkin: WeeklyCheckIn) -> None:
        query = text("""
            UPDATE check_ins
            SET status = :status, submitted_at = :submitted_at, updated_at = now()
            WHERE id = :id AND organization_id = :organization_id AND deleted_at IS NULL
        """)
        await self._session.execute(query, {
            "id": checkin.id,
            "status": checkin.status,
            "submitted_at": checkin.submitted_at,
            "organization_id": checkin.organization_id,
        })
        await self._session.commit()

    @staticmethod
    def _to_entity(row) -> WeeklyCheckIn:
        return WeeklyCheckIn(
            id=row.id,
            organization_id=row.organization_id,
            employee_id=row.employee_id,
            week_start=row.week_start,
            status=row.status,
            submitted_at=row.submitted_at,
            created_at=row.created_at,
            updated_at=row.updated_at,
        )
