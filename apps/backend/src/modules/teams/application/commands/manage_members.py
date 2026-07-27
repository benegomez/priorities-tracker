from dataclasses import dataclass
from uuid import UUID

from src.modules.teams.domain.repositories.team_admin_repository import TeamAdminRepository
from src.shared.exceptions.base import BusinessRuleViolation


@dataclass
class AddMemberCommand:
    team_id: UUID
    user_id: UUID
    organization_id: UUID


class AddMemberUseCase:
    def __init__(self, repo: TeamAdminRepository) -> None:
        self._repo = repo

    async def execute(self, command: AddMemberCommand) -> None:
        if not await self._repo.user_exists(command.user_id, command.organization_id):
            raise ValueError(f"User {command.user_id} not found in organization")

        team = await self._repo.get_by_id(command.team_id, command.organization_id)
        if team is None:
            raise ValueError(f"Team {command.team_id} not found")

        members = await self._repo.get_members(command.team_id, command.organization_id)
        if any(m.id == command.user_id for m in members):
            raise BusinessRuleViolation("BR-NEW-07: User is already a member of this team")

        # BR-NEW-07: assign removes from previous team automatically (UPDATE sets team_id)
        await self._repo.add_member(command.team_id, command.user_id, command.organization_id)


@dataclass
class RemoveMemberCommand:
    team_id: UUID
    user_id: UUID
    organization_id: UUID


class RemoveMemberUseCase:
    def __init__(self, repo: TeamAdminRepository) -> None:
        self._repo = repo

    async def execute(self, command: RemoveMemberCommand) -> None:
        removed = await self._repo.remove_member(command.team_id, command.user_id, command.organization_id)
        if not removed:
            raise ValueError(f"User {command.user_id} is not a member of team {command.team_id}")
