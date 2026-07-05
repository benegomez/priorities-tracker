from uuid import UUID

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from src.modules.priorities.domain.entities.task import Task
from src.modules.priorities.domain.repositories.task_repository import TaskRepository


class TaskRepositoryImpl(TaskRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def save(self, task: Task) -> None:
        query = text("""
            INSERT INTO tasks (id, organization_id, priority_id, title, description, status)
            VALUES (:id, :organization_id, :priority_id, :title, :description, :status)
        """)
        await self._session.execute(query, {
            "id": task.id,
            "organization_id": task.organization_id,
            "priority_id": task.priority_id,
            "title": task.title,
            "description": task.description,
            "status": task.status,
        })
        await self._session.commit()

    async def get_by_id(self, task_id: UUID, organization_id: UUID) -> Task | None:
        query = text("""
            SELECT id, organization_id, priority_id, title, description, status, created_at, updated_at
            FROM tasks
            WHERE id = :id AND organization_id = :organization_id AND deleted_at IS NULL
        """)
        result = await self._session.execute(query, {"id": task_id, "organization_id": organization_id})
        row = result.one_or_none()
        return self._to_entity(row) if row else None

    @staticmethod
    def _to_entity(row) -> Task:
        return Task(
            id=row.id,
            organization_id=row.organization_id,
            priority_id=row.priority_id,
            title=row.title,
            description=row.description,
            status=row.status,
            created_at=row.created_at,
            updated_at=row.updated_at,
        )
