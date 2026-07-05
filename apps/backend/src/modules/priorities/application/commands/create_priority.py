from dataclasses import dataclass
from uuid import UUID, uuid4

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from src.modules.checkin.domain.repositories.checkin_repository import CheckInRepository
from src.modules.priorities.domain.entities.priority import Priority
from src.modules.priorities.domain.repositories.priority_repository import PriorityRepository
from src.shared.exceptions.base import AuthorizationException, BusinessRuleViolation, ValidationException


@dataclass
class CreatePriorityCommand:
    checkin_id: UUID
    phase_id: UUID
    title: str
    description: str | None
    priority_level: str
    employee_id: UUID
    organization_id: UUID


class CreatePriorityUseCase:
    def __init__(
        self,
        priority_repo: PriorityRepository,
        checkin_repo: CheckInRepository,
        session: AsyncSession,
    ) -> None:
        self._priority_repo = priority_repo
        self._checkin_repo = checkin_repo
        self._session = session

    async def execute(self, command: CreatePriorityCommand) -> Priority:
        # Validate checkin exists and belongs to employee
        checkin = await self._checkin_repo.get_by_id(command.checkin_id, command.organization_id)
        if checkin is None:
            raise BusinessRuleViolation("Check-in not found")

        # BR-013: employee can only add priorities to their own check-in
        if checkin.employee_id != command.employee_id:
            raise AuthorizationException("BR-013: Cannot add priorities to another employee's check-in")

        # Check-in must be in draft or submitted to accept new priorities
        if checkin.status not in ("draft", "submitted"):
            raise BusinessRuleViolation("Cannot add priorities to a closed check-in")

        # If submitted, verify no checkout exists (locks the check-in)
        if checkin.status == "submitted":
            checkout_check = await self._session.execute(
                text("""
                    SELECT id FROM check_outs
                    WHERE employee_id = :employee_id AND week_start = :week_start
                      AND organization_id = :organization_id AND deleted_at IS NULL
                """),
                {"employee_id": command.employee_id, "week_start": checkin.week_start, "organization_id": command.organization_id},
            )
            if checkout_check.one_or_none() is not None:
                raise BusinessRuleViolation("Check-In is locked by an existing Check-Out")

        # BR-003 + BR-004: validate phase exists, belongs to org, and project is active
        await self._validate_phase(command.phase_id, command.organization_id)

        priority = Priority(
            id=uuid4(),
            organization_id=command.organization_id,
            checkin_id=command.checkin_id,
            phase_id=command.phase_id,
            owner_id=command.employee_id,
            week_start=checkin.week_start,
            title=command.title,
            description=command.description,
            priority_level=command.priority_level,
        )

        await self._priority_repo.save(priority)
        return priority

    async def _validate_phase(self, phase_id: UUID, organization_id: UUID) -> None:
        query = text("""
            SELECT pp.id, p.status as project_status
            FROM project_phases pp
            JOIN projects p ON pp.project_id = p.id
            WHERE pp.id = :phase_id
              AND pp.organization_id = :organization_id
              AND pp.deleted_at IS NULL
              AND p.deleted_at IS NULL
        """)
        result = await self._session.execute(query, {"phase_id": phase_id, "organization_id": organization_id})
        row = result.one_or_none()

        if row is None:
            raise AuthorizationException("BR-016: Phase not found or belongs to another organization")

        if row.project_status != "active":
            raise BusinessRuleViolation("BR-004: Phase belongs to a project that is not active")
