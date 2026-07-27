from dataclasses import dataclass
from uuid import UUID

from src.modules.teams.domain.entities.team import TeamDetail
from src.modules.teams.domain.repositories.team_admin_repository import TeamAdminRepository
from src.shared.exceptions.base import BusinessRuleViolation


@dataclass
class CreateTeamCommand:
    organization_id: UUID
    name: str
    manager_id: UUID | None


class CreateTeamUseCase:
    def __init__(self, repo: TeamAdminRepository) -> None:
        self._repo = repo

    async def execute(self, command: CreateTeamCommand) -> TeamDetail:
        if await self._repo.name_exists(command.name, command.organization_id):
            raise BusinessRuleViolation("BR-NEW-05: Team name already exists in this organization")

        if command.manager_id and not await self._repo.manager_valid(command.manager_id, command.organization_id):
            raise ValueError(f"Manager {command.manager_id} not found or has invalid role")

        return await self._repo.create(
            organization_id=command.organization_id,
            name=command.name,
            manager_id=command.manager_id,
        )


@dataclass
class UpdateTeamCommand:
    team_id: UUID
    organization_id: UUID
    name: str | None
    manager_id: UUID | None


class UpdateTeamUseCase:
    def __init__(self, repo: TeamAdminRepository) -> None:
        self._repo = repo

    async def execute(self, command: UpdateTeamCommand) -> TeamDetail:
        if command.name and await self._repo.name_exists(command.name, command.organization_id, exclude_id=command.team_id):
            raise BusinessRuleViolation("BR-NEW-05: Team name already exists in this organization")

        if command.manager_id and not await self._repo.manager_valid(command.manager_id, command.organization_id):
            raise ValueError(f"Manager {command.manager_id} not found or has invalid role")

        team = await self._repo.update(
            team_id=command.team_id,
            organization_id=command.organization_id,
            name=command.name,
            manager_id=command.manager_id,
        )
        if team is None:
            raise ValueError(f"Team {command.team_id} not found")
        return team
