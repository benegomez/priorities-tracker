from datetime import date
from uuid import UUID

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from src.modules.checkout.domain.entities.checkout import WeeklyCheckOut
from src.modules.checkout.domain.repositories.checkout_repository import CheckOutRepository


class CheckOutRepositoryImpl(CheckOutRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def save(self, checkout: WeeklyCheckOut) -> None:
        await self._session.execute(
            text("""
                INSERT INTO check_outs (id, organization_id, employee_id, checkin_id, week_start, status, submitted_at, notes, lessons_learned)
                VALUES (:id, :organization_id, :employee_id, :checkin_id, :week_start, :status, :submitted_at, :notes, :lessons_learned)
            """),
            {
                "id": checkout.id,
                "organization_id": checkout.organization_id,
                "employee_id": checkout.employee_id,
                "checkin_id": checkout.checkin_id,
                "week_start": checkout.week_start,
                "status": checkout.status,
                "submitted_at": checkout.submitted_at,
                "notes": checkout.notes,
                "lessons_learned": checkout.lessons_learned,
            },
        )
        await self._session.commit()

    async def get_by_id(self, checkout_id: UUID, organization_id: UUID) -> WeeklyCheckOut | None:
        result = await self._session.execute(
            text("""
                SELECT id, organization_id, employee_id, checkin_id, week_start, status, submitted_at, notes, lessons_learned, created_at, updated_at
                FROM check_outs
                WHERE id = :id AND organization_id = :organization_id AND deleted_at IS NULL
            """),
            {"id": checkout_id, "organization_id": organization_id},
        )
        row = result.one_or_none()
        return self._to_entity(row) if row else None

    async def get_by_employee_and_week(self, employee_id: UUID, week_start: date, organization_id: UUID) -> WeeklyCheckOut | None:
        result = await self._session.execute(
            text("""
                SELECT id, organization_id, employee_id, checkin_id, week_start, status, submitted_at, notes, lessons_learned, created_at, updated_at
                FROM check_outs
                WHERE employee_id = :employee_id AND week_start = :week_start
                  AND organization_id = :organization_id AND deleted_at IS NULL
            """),
            {"employee_id": employee_id, "week_start": week_start, "organization_id": organization_id},
        )
        row = result.one_or_none()
        return self._to_entity(row) if row else None

    async def update(self, checkout: WeeklyCheckOut) -> None:
        await self._session.execute(
            text("""
                UPDATE check_outs
                SET status = :status, submitted_at = :submitted_at, notes = :notes,
                    lessons_learned = :lessons_learned, updated_at = now()
                WHERE id = :id AND organization_id = :organization_id AND deleted_at IS NULL
            """),
            {
                "id": checkout.id,
                "status": checkout.status,
                "submitted_at": checkout.submitted_at,
                "notes": checkout.notes,
                "lessons_learned": checkout.lessons_learned,
                "organization_id": checkout.organization_id,
            },
        )
        await self._session.commit()

    @staticmethod
    def _to_entity(row) -> WeeklyCheckOut:
        return WeeklyCheckOut(
            id=row.id,
            organization_id=row.organization_id,
            employee_id=row.employee_id,
            checkin_id=row.checkin_id,
            week_start=row.week_start,
            status=row.status,
            submitted_at=row.submitted_at,
            notes=row.notes,
            lessons_learned=row.lessons_learned,
            created_at=row.created_at,
            updated_at=row.updated_at,
        )
