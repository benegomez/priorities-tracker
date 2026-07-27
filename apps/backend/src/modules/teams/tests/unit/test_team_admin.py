"""Unit tests for admin team management use cases."""
import pytest
from unittest.mock import AsyncMock, MagicMock
from uuid import UUID, uuid4

from src.modules.teams.application.commands.create_update_team import (
    CreateTeamCommand,
    CreateTeamUseCase,
    UpdateTeamCommand,
    UpdateTeamUseCase,
)
from src.modules.teams.application.commands.manage_members import (
    AddMemberCommand,
    AddMemberUseCase,
    RemoveMemberCommand,
    RemoveMemberUseCase,
)
from src.modules.teams.domain.entities.team import TeamDetail, TeamMemberDetail
from src.shared.exceptions.base import BusinessRuleViolation

ORG_ID = UUID("00000000-0000-0000-0000-000000000001")
TEAM_ID = uuid4()
MANAGER_ID = uuid4()
USER_ID = uuid4()


def _mock_repo(**overrides):
    repo = AsyncMock()
    repo.name_exists.return_value = False
    repo.manager_valid.return_value = True
    repo.user_exists.return_value = True
    repo.get_by_id.return_value = TeamDetail(
        id=TEAM_ID, organization_id=ORG_ID, name="Team A",
        manager_id=MANAGER_ID, manager_name="Manager One", member_count=0,
    )
    repo.get_members.return_value = []
    repo.add_member.return_value = True
    repo.remove_member.return_value = True
    for k, v in overrides.items():
        setattr(repo, k, v)
    return repo


class TestCreateTeamUseCase:
    @pytest.mark.asyncio
    async def test_creates_team_successfully(self):
        repo = _mock_repo()
        expected = TeamDetail(
            id=TEAM_ID, organization_id=ORG_ID, name="Team A",
            manager_id=MANAGER_ID, manager_name="Manager One", member_count=0,
        )
        repo.create = AsyncMock(return_value=expected)
        result = await CreateTeamUseCase(repo).execute(
            CreateTeamCommand(organization_id=ORG_ID, name="Team A", manager_id=MANAGER_ID)
        )
        assert result.name == "Team A"
        repo.create.assert_called_once()

    @pytest.mark.asyncio
    async def test_raises_409_on_duplicate_name(self):
        repo = _mock_repo()
        repo.name_exists = AsyncMock(return_value=True)
        with pytest.raises(BusinessRuleViolation, match="BR-NEW-05"):
            await CreateTeamUseCase(repo).execute(
                CreateTeamCommand(organization_id=ORG_ID, name="Team A", manager_id=None)
            )

    @pytest.mark.asyncio
    async def test_raises_404_on_invalid_manager(self):
        repo = _mock_repo()
        repo.manager_valid = AsyncMock(return_value=False)
        with pytest.raises(ValueError):
            await CreateTeamUseCase(repo).execute(
                CreateTeamCommand(organization_id=ORG_ID, name="Team B", manager_id=MANAGER_ID)
            )

    @pytest.mark.asyncio
    async def test_creates_team_without_manager(self):
        repo = _mock_repo()
        await CreateTeamUseCase(repo).execute(
            CreateTeamCommand(organization_id=ORG_ID, name="Team C", manager_id=None)
        )
        repo.manager_valid.assert_not_called()


class TestUpdateTeamUseCase:
    @pytest.mark.asyncio
    async def test_updates_team_successfully(self):
        repo = _mock_repo()
        result = await UpdateTeamUseCase(repo).execute(
            UpdateTeamCommand(team_id=TEAM_ID, organization_id=ORG_ID, name="New Name", manager_id=None)
        )
        assert result is not None

    @pytest.mark.asyncio
    async def test_raises_409_on_duplicate_name(self):
        repo = _mock_repo()
        repo.name_exists = AsyncMock(return_value=True)
        with pytest.raises(BusinessRuleViolation, match="BR-NEW-05"):
            await UpdateTeamUseCase(repo).execute(
                UpdateTeamCommand(team_id=TEAM_ID, organization_id=ORG_ID, name="Existing", manager_id=None)
            )

    @pytest.mark.asyncio
    async def test_raises_404_when_team_not_found(self):
        repo = _mock_repo()
        repo.update = AsyncMock(return_value=None)
        with pytest.raises(ValueError):
            await UpdateTeamUseCase(repo).execute(
                UpdateTeamCommand(team_id=TEAM_ID, organization_id=ORG_ID, name="X", manager_id=None)
            )


class TestAddMemberUseCase:
    @pytest.mark.asyncio
    async def test_adds_member_successfully(self):
        repo = _mock_repo()
        await AddMemberUseCase(repo).execute(
            AddMemberCommand(team_id=TEAM_ID, user_id=USER_ID, organization_id=ORG_ID)
        )
        repo.add_member.assert_called_once_with(TEAM_ID, USER_ID, ORG_ID)

    @pytest.mark.asyncio
    async def test_raises_404_when_user_not_found(self):
        repo = _mock_repo()
        repo.user_exists = AsyncMock(return_value=False)
        with pytest.raises(ValueError):
            await AddMemberUseCase(repo).execute(
                AddMemberCommand(team_id=TEAM_ID, user_id=USER_ID, organization_id=ORG_ID)
            )

    @pytest.mark.asyncio
    async def test_raises_409_when_already_member(self):
        repo = _mock_repo()
        repo.get_members = AsyncMock(return_value=[
            TeamMemberDetail(id=USER_ID, first_name="Ana", last_name="G", role="employee", status="active")
        ])
        with pytest.raises(BusinessRuleViolation, match="BR-NEW-07"):
            await AddMemberUseCase(repo).execute(
                AddMemberCommand(team_id=TEAM_ID, user_id=USER_ID, organization_id=ORG_ID)
            )


class TestRemoveMemberUseCase:
    @pytest.mark.asyncio
    async def test_removes_member_successfully(self):
        repo = _mock_repo()
        await RemoveMemberUseCase(repo).execute(
            RemoveMemberCommand(team_id=TEAM_ID, user_id=USER_ID, organization_id=ORG_ID)
        )
        repo.remove_member.assert_called_once()

    @pytest.mark.asyncio
    async def test_raises_404_when_not_member(self):
        repo = _mock_repo()
        repo.remove_member = AsyncMock(return_value=False)
        with pytest.raises(ValueError):
            await RemoveMemberUseCase(repo).execute(
                RemoveMemberCommand(team_id=TEAM_ID, user_id=USER_ID, organization_id=ORG_ID)
            )
