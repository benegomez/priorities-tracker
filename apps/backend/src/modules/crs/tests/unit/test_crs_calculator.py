import pytest
from unittest.mock import AsyncMock, patch
from uuid import uuid4
from datetime import date

from src.modules.crs.application.services.crs_calculator import CRSCalculationService, CRSResult


ORG_ID = uuid4()
EMP_ID = uuid4()
CHECKOUT_ID = uuid4()
WEEK = date(2026, 7, 5)


def make_service(historical_scores: list[float] | None = None):
    mock_repo = AsyncMock()
    mock_repo.get_last_n_scores.return_value = historical_scores or []
    mock_repo.save.return_value = None
    return CRSCalculationService(crs_repo=mock_repo), mock_repo


class TestCRSCalculatorScore:
    @pytest.mark.asyncio
    async def test_all_completed_returns_100(self):
        svc, _ = make_service([100, 100, 100, 100])
        result = await svc.calculate(EMP_ID, ORG_ID, CHECKOUT_ID, WEEK, 3, 3, 0, 5, 5)
        assert result.score == 100.0

    @pytest.mark.asyncio
    async def test_none_completed_returns_low_score(self):
        svc, _ = make_service([50, 50, 50, 50])
        result = await svc.calculate(EMP_ID, ORG_ID, CHECKOUT_ID, WEEK, 3, 0, 3, 5, 0)
        assert result.score < 20

    @pytest.mark.asyncio
    async def test_zero_priorities_uses_100(self):
        svc, _ = make_service([80, 80, 80, 80])
        result = await svc.calculate(EMP_ID, ORG_ID, CHECKOUT_ID, WEEK, 0, 0, 0, 5, 5)
        # priorities=100, tasks=100, consistency=80, carryover=100
        # 0.40*100 + 0.30*100 + 0.20*80 + 0.10*100 = 40+30+16+10 = 96
        assert result.score == 96.0

    @pytest.mark.asyncio
    async def test_zero_tasks_uses_100(self):
        svc, _ = make_service([80, 80, 80, 80])
        result = await svc.calculate(EMP_ID, ORG_ID, CHECKOUT_ID, WEEK, 3, 3, 0, 0, 0)
        # priorities=100, tasks=100, consistency=80, carryover=100
        assert result.score == 96.0

    @pytest.mark.asyncio
    async def test_first_week_reponders_without_history(self):
        svc, _ = make_service([])  # no history
        result = await svc.calculate(EMP_ID, ORG_ID, CHECKOUT_ID, WEEK, 4, 3, 1, 6, 5)
        # priorities: 3/4*100=75, tasks: 5/6*100=83.33, carryover: (1-1/4)*100=75
        # 0.50*75 + 0.375*83.33 + 0.125*75 = 37.5 + 31.25 + 9.375 = 78.125
        assert abs(result.score - 78.12) < 0.1

    @pytest.mark.asyncio
    async def test_with_4_weeks_history_uses_average(self):
        svc, _ = make_service([80, 70, 90, 60])  # avg=75
        result = await svc.calculate(EMP_ID, ORG_ID, CHECKOUT_ID, WEEK, 2, 2, 0, 4, 4)
        # priorities=100, tasks=100, consistency=75, carryover=100
        # 0.40*100 + 0.30*100 + 0.20*75 + 0.10*100 = 40+30+15+10 = 95
        assert result.score == 95.0

    @pytest.mark.asyncio
    async def test_with_2_weeks_history_averages_available(self):
        svc, _ = make_service([80, 60])  # avg=70
        result = await svc.calculate(EMP_ID, ORG_ID, CHECKOUT_ID, WEEK, 2, 2, 0, 4, 4)
        # priorities=100, tasks=100, consistency=70, carryover=100
        # 0.40*100 + 0.30*100 + 0.20*70 + 0.10*100 = 40+30+14+10 = 94
        assert result.score == 94.0

    @pytest.mark.asyncio
    async def test_carried_over_penalizes_score(self):
        svc, _ = make_service([80, 80, 80, 80])
        result = await svc.calculate(EMP_ID, ORG_ID, CHECKOUT_ID, WEEK, 4, 2, 2, 4, 4)
        # priorities: 2/4*100=50, tasks=100, consistency=80, carryover: (1-2/4)*100=50
        # 0.40*50 + 0.30*100 + 0.20*80 + 0.10*50 = 20+30+16+5 = 71
        assert result.score == 71.0

    @pytest.mark.asyncio
    async def test_all_carried_gives_zero_arrastre(self):
        svc, _ = make_service([80, 80, 80, 80])
        result = await svc.calculate(EMP_ID, ORG_ID, CHECKOUT_ID, WEEK, 3, 0, 3, 0, 0)
        # priorities: 0/3*100=0, tasks=100(0 total), consistency=80, carryover: (1-3/3)*100=0
        # 0.40*0 + 0.30*100 + 0.20*80 + 0.10*0 = 0+30+16+0 = 46
        assert result.score == 46.0


class TestCRSTrend:
    @pytest.mark.asyncio
    async def test_improving_when_above_average_plus_5(self):
        svc, _ = make_service([70, 70, 70, 70])  # avg=70
        # Score will be high (all completed) → diff > 5
        result = await svc.calculate(EMP_ID, ORG_ID, CHECKOUT_ID, WEEK, 2, 2, 0, 2, 2)
        assert result.trend == "improving"

    @pytest.mark.asyncio
    async def test_declining_when_below_average_minus_5(self):
        svc, _ = make_service([90, 90, 90, 90])  # avg=90
        # Score will be low (none completed) → diff < -5
        result = await svc.calculate(EMP_ID, ORG_ID, CHECKOUT_ID, WEEK, 3, 0, 3, 3, 0)
        assert result.trend == "declining"

    @pytest.mark.asyncio
    async def test_stable_within_5_points(self):
        svc, _ = make_service([95, 95, 95, 95])  # avg=95
        # Score ~96 (all completed + consistency 95) → diff ~1 → stable
        result = await svc.calculate(EMP_ID, ORG_ID, CHECKOUT_ID, WEEK, 2, 2, 0, 2, 2)
        assert result.trend == "stable"

    @pytest.mark.asyncio
    async def test_stable_on_first_week(self):
        svc, _ = make_service([])
        result = await svc.calculate(EMP_ID, ORG_ID, CHECKOUT_ID, WEEK, 2, 2, 0, 2, 2)
        assert result.trend == "stable"


class TestCRSRiskLevel:
    @pytest.mark.asyncio
    async def test_low_above_75(self):
        svc, _ = make_service([80, 80, 80, 80])
        result = await svc.calculate(EMP_ID, ORG_ID, CHECKOUT_ID, WEEK, 2, 2, 0, 2, 2)
        assert result.risk_level == "low"

    @pytest.mark.asyncio
    async def test_moderate_between_60_and_74(self):
        svc, _ = make_service([60, 60, 60, 60])
        # Need score between 60-74
        result = await svc.calculate(EMP_ID, ORG_ID, CHECKOUT_ID, WEEK, 4, 2, 2, 4, 2)
        # priorities: 50, tasks: 50, consistency: 60, carryover: 50
        # 0.40*50 + 0.30*50 + 0.20*60 + 0.10*50 = 20+15+12+5 = 52 → high actually
        # Let's adjust: 4 priorities, 3 completed, 1 carried
        result = await svc.calculate(EMP_ID, ORG_ID, CHECKOUT_ID, WEEK, 4, 3, 1, 4, 3)
        # priorities: 75, tasks: 75, consistency: 60, carryover: 75
        # 0.40*75 + 0.30*75 + 0.20*60 + 0.10*75 = 30+22.5+12+7.5 = 72 → moderate
        assert result.risk_level == "moderate"

    @pytest.mark.asyncio
    async def test_high_below_60(self):
        svc, _ = make_service([40, 40, 40, 40])
        result = await svc.calculate(EMP_ID, ORG_ID, CHECKOUT_ID, WEEK, 4, 1, 3, 4, 1)
        # priorities: 25, tasks: 25, consistency: 40, carryover: 25
        # 0.40*25 + 0.30*25 + 0.20*40 + 0.10*25 = 10+7.5+8+2.5 = 28
        assert result.risk_level == "high"


class TestCRSPersistence:
    @pytest.mark.asyncio
    async def test_formula_version_stored(self):
        svc, mock_repo = make_service([])
        result = await svc.calculate(EMP_ID, ORG_ID, CHECKOUT_ID, WEEK, 2, 2, 0, 2, 2)
        assert result.formula_version == "v1.0"
        mock_repo.save.assert_called_once()
        call_kwargs = mock_repo.save.call_args[1]
        assert call_kwargs["formula_version"] == "v1.0"
