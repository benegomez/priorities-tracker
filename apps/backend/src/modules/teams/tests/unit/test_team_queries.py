"""Unit tests for teams module — manager team visibility."""
import pytest
from datetime import date
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import UUID, uuid4

from fastapi import HTTPException


MANAGER_ID = UUID("00000000-0000-0000-0001-000000000002")
ORG_ID = UUID("00000000-0000-0000-0000-000000000001")
EMPLOYEE_ID = UUID("00000000-0000-0000-0001-000000000003")
OTHER_EMPLOYEE_ID = UUID("00000000-0000-0000-0002-000000000001")


class FakeRow:
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


class TestValidateDirectReport:
    @pytest.mark.asyncio
    async def test_raises_403_for_non_report(self):
        from src.modules.teams.infrastructure.repositories.team_repository_impl import TeamRepositoryImpl

        session = AsyncMock()
        result_mock = MagicMock()
        result_mock.one_or_none.return_value = None
        session.execute.return_value = result_mock

        repo = TeamRepositoryImpl(session)
        with pytest.raises(HTTPException) as exc_info:
            await repo.validate_direct_report(OTHER_EMPLOYEE_ID, MANAGER_ID, ORG_ID)
        assert exc_info.value.status_code == 403

    @pytest.mark.asyncio
    async def test_raises_403_cross_org(self):
        from src.modules.teams.infrastructure.repositories.team_repository_impl import TeamRepositoryImpl

        session = AsyncMock()
        result_mock = MagicMock()
        result_mock.one_or_none.return_value = None
        session.execute.return_value = result_mock

        other_org = UUID("00000000-0000-0000-0000-000000000099")
        repo = TeamRepositoryImpl(session)
        with pytest.raises(HTTPException) as exc_info:
            await repo.validate_direct_report(EMPLOYEE_ID, MANAGER_ID, other_org)
        assert exc_info.value.status_code == 403

    @pytest.mark.asyncio
    async def test_returns_row_for_valid_report(self):
        from src.modules.teams.infrastructure.repositories.team_repository_impl import TeamRepositoryImpl

        session = AsyncMock()
        row = FakeRow(id=EMPLOYEE_ID, first_name="Employee", last_name="Alpha")
        result_mock = MagicMock()
        result_mock.one_or_none.return_value = row
        session.execute.return_value = result_mock

        repo = TeamRepositoryImpl(session)
        result = await repo.validate_direct_report(EMPLOYEE_ID, MANAGER_ID, ORG_ID)
        assert result.id == EMPLOYEE_ID


class TestGetDirectReports:
    @pytest.mark.asyncio
    async def test_returns_active_direct_reports(self):
        from src.modules.teams.infrastructure.repositories.team_repository_impl import TeamRepositoryImpl

        session = AsyncMock()
        rows = [
            FakeRow(id=EMPLOYEE_ID, first_name="Employee", last_name="Alpha", email="e@org.com"),
        ]
        result_mock = MagicMock()
        result_mock.fetchall.return_value = rows
        session.execute.return_value = result_mock

        repo = TeamRepositoryImpl(session)
        result = await repo.get_direct_reports(MANAGER_ID, ORG_ID)
        assert len(result) == 1
        assert result[0].first_name == "Employee"

    @pytest.mark.asyncio
    async def test_returns_empty_when_no_reports(self):
        from src.modules.teams.infrastructure.repositories.team_repository_impl import TeamRepositoryImpl

        session = AsyncMock()
        result_mock = MagicMock()
        result_mock.fetchall.return_value = []
        session.execute.return_value = result_mock

        repo = TeamRepositoryImpl(session)
        result = await repo.get_direct_reports(MANAGER_ID, ORG_ID)
        assert result == []


class TestGetLatestCRSBatch:
    @pytest.mark.asyncio
    async def test_returns_crs_when_available(self):
        from src.modules.teams.infrastructure.repositories.team_repository_impl import TeamRepositoryImpl

        session = AsyncMock()
        rows = [FakeRow(employee_id=EMPLOYEE_ID, score=85.5, trend="improving", risk_level="low")]
        result_mock = MagicMock()
        result_mock.fetchall.return_value = rows
        session.execute.return_value = result_mock

        repo = TeamRepositoryImpl(session)
        result = await repo.get_latest_crs_batch([EMPLOYEE_ID], ORG_ID)
        assert EMPLOYEE_ID in result
        assert result[EMPLOYEE_ID].score == 85.5

    @pytest.mark.asyncio
    async def test_returns_empty_dict_when_no_crs(self):
        from src.modules.teams.infrastructure.repositories.team_repository_impl import TeamRepositoryImpl

        session = AsyncMock()
        result_mock = MagicMock()
        result_mock.fetchall.return_value = []
        session.execute.return_value = result_mock

        repo = TeamRepositoryImpl(session)
        result = await repo.get_latest_crs_batch([EMPLOYEE_ID], ORG_ID)
        assert result == {}

    @pytest.mark.asyncio
    async def test_returns_empty_for_empty_ids(self):
        from src.modules.teams.infrastructure.repositories.team_repository_impl import TeamRepositoryImpl

        session = AsyncMock()
        repo = TeamRepositoryImpl(session)
        result = await repo.get_latest_crs_batch([], ORG_ID)
        assert result == {}


class TestWeekStatusBatch:
    @pytest.mark.asyncio
    async def test_returns_checkin_status(self):
        from src.modules.teams.infrastructure.repositories.team_repository_impl import TeamRepositoryImpl

        session = AsyncMock()
        rows = [FakeRow(employee_id=EMPLOYEE_ID, status="submitted")]
        result_mock = MagicMock()
        result_mock.fetchall.return_value = rows
        session.execute.return_value = result_mock

        repo = TeamRepositoryImpl(session)
        result = await repo.get_week_checkins_batch([EMPLOYEE_ID], ORG_ID, date.today())
        assert result[EMPLOYEE_ID] == "submitted"

    @pytest.mark.asyncio
    async def test_returns_empty_for_no_checkins(self):
        from src.modules.teams.infrastructure.repositories.team_repository_impl import TeamRepositoryImpl

        session = AsyncMock()
        result_mock = MagicMock()
        result_mock.fetchall.return_value = []
        session.execute.return_value = result_mock

        repo = TeamRepositoryImpl(session)
        result = await repo.get_week_checkins_batch([EMPLOYEE_ID], ORG_ID, date.today())
        assert result == {}
