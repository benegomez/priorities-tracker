"""Unit tests for GenerateTeamSummaryUseCase."""
import pytest
from datetime import date, datetime, timezone
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import UUID

from src.modules.ai_insights.application.commands.generate_team_summary import (
    GenerateTeamSummaryUseCase,
    TeamSummaryResult,
)


ORG_ID = UUID("00000000-0000-0000-0000-000000000001")
MANAGER_ID = UUID("00000000-0000-0000-0001-000000000002")


def _make_member(id_str: str, first: str, last: str):
    m = MagicMock()
    m.id = UUID(id_str)
    m.first_name = first
    m.last_name = last
    return m


def _make_crs(score: float, trend: str, risk_level: str):
    c = MagicMock()
    c.score = score
    c.trend = trend
    c.risk_level = risk_level
    return c


MEMBERS = [
    _make_member("00000000-0000-0000-0001-000000000003", "Employee", "Alpha"),
    _make_member("00000000-0000-0000-0001-000000000005", "Carlos", "Rivera"),
]

CRS_BATCH = {
    UUID("00000000-0000-0000-0001-000000000003"): _make_crs(67.0, "stable", "moderate"),
    UUID("00000000-0000-0000-0001-000000000005"): _make_crs(80.5, "declining", "low"),
}

CRS_EXTENDED = {
    UUID("00000000-0000-0000-0001-000000000003"): {"priorities_total": 4, "priorities_completed": 2, "tasks_total": 9, "tasks_completed": 8},
    UUID("00000000-0000-0000-0001-000000000005"): {"priorities_total": 3, "priorities_completed": 2, "tasks_total": 6, "tasks_completed": 6},
}


@pytest.fixture
def mock_session():
    return AsyncMock()


@pytest.fixture
def mock_openai():
    client = MagicMock()
    client.is_configured = True
    client.model_name = "gpt-4o-mini"
    client.generate = AsyncMock(return_value="Resumen generado por IA.")
    return client


@pytest.fixture
def use_case(mock_session, mock_openai):
    uc = GenerateTeamSummaryUseCase(session=mock_session, openai_client=mock_openai)
    uc._team_repo = MagicMock()
    uc._team_repo.get_direct_reports = AsyncMock(return_value=MEMBERS)
    uc._team_repo.get_latest_crs_batch = AsyncMock(return_value=CRS_BATCH)
    uc._summary_repo = MagicMock()
    uc._summary_repo.get_cached = AsyncMock(return_value=None)
    uc._summary_repo.save = AsyncMock()
    uc._summary_repo.delete = AsyncMock()
    uc._get_crs_with_counts = AsyncMock(return_value=CRS_EXTENDED)
    return uc


@pytest.mark.asyncio
async def test_generate_summary_calls_openai_when_no_cache(use_case, mock_openai):
    result = await use_case.execute(MANAGER_ID, ORG_ID, regenerate=False)
    assert result.fallback is False
    assert result.cached is False
    assert result.model == "gpt-4o-mini"
    assert result.summary == "Resumen generado por IA."
    mock_openai.generate.assert_called_once()


@pytest.mark.asyncio
async def test_generate_summary_returns_cached_when_exists(use_case):
    use_case._summary_repo.get_cached = AsyncMock(return_value={
        "summary": "Cached summary",
        "model": "gpt-4o-mini",
        "data_snapshot": {"team_size": 2, "week_start": str(date.today()), "avg_crs": 73.0, "total_priorities": 7, "completed_priorities": 4, "completion_rate": 57.1},
        "fallback": False,
        "generated_at": datetime.now(timezone.utc),
    })
    result = await use_case.execute(MANAGER_ID, ORG_ID, regenerate=False)
    assert result.cached is True
    assert result.summary == "Cached summary"


@pytest.mark.asyncio
async def test_generate_summary_regenerate_deletes_cache(use_case, mock_openai):
    result = await use_case.execute(MANAGER_ID, ORG_ID, regenerate=True)
    use_case._summary_repo.delete.assert_called_once()
    assert result.cached is False
    mock_openai.generate.assert_called_once()


@pytest.mark.asyncio
async def test_generate_summary_fallback_when_openai_fails(use_case, mock_openai):
    mock_openai.generate = AsyncMock(return_value=None)
    result = await use_case.execute(MANAGER_ID, ORG_ID, regenerate=False)
    assert result.fallback is True
    assert result.cached is False
    assert result.model is None
    assert "Resumen automático" in result.summary


@pytest.mark.asyncio
async def test_generate_summary_fallback_when_no_api_key(mock_session):
    client = MagicMock()
    client.is_configured = False
    client.generate = AsyncMock(return_value=None)
    uc = GenerateTeamSummaryUseCase(session=mock_session, openai_client=client)
    uc._team_repo = MagicMock()
    uc._team_repo.get_direct_reports = AsyncMock(return_value=MEMBERS)
    uc._team_repo.get_latest_crs_batch = AsyncMock(return_value=CRS_BATCH)
    uc._summary_repo = MagicMock()
    uc._summary_repo.get_cached = AsyncMock(return_value=None)
    uc._summary_repo.save = AsyncMock()
    uc._get_crs_with_counts = AsyncMock(return_value=CRS_EXTENDED)
    result = await uc.execute(MANAGER_ID, ORG_ID)
    assert result.fallback is True


@pytest.mark.asyncio
async def test_fallback_not_persisted_in_cache(use_case, mock_openai):
    mock_openai.generate = AsyncMock(return_value=None)
    await use_case.execute(MANAGER_ID, ORG_ID)
    use_case._summary_repo.save.assert_not_called()


@pytest.mark.asyncio
async def test_generate_summary_empty_team(use_case):
    use_case._team_repo.get_direct_reports = AsyncMock(return_value=[])
    result = await use_case.execute(MANAGER_ID, ORG_ID)
    assert "No tienes miembros" in result.summary
    assert result.fallback is True


@pytest.mark.asyncio
async def test_data_snapshot_calculated_correctly(use_case):
    result = await use_case.execute(MANAGER_ID, ORG_ID)
    snap = result.data_snapshot
    assert snap["team_size"] == 2
    assert snap["total_priorities"] == 7
    assert snap["completed_priorities"] == 4
    assert snap["avg_crs"] == 73.8  # (67+80.5)/2


@pytest.mark.asyncio
async def test_prompt_contains_team_data(use_case, mock_openai):
    await use_case.execute(MANAGER_ID, ORG_ID)
    call_args = mock_openai.generate.call_args
    user_prompt = call_args[0][1]
    assert "Employee Alpha" in user_prompt
    assert "Carlos Rivera" in user_prompt
    assert "67.0" in user_prompt
    assert "80.5" in user_prompt
