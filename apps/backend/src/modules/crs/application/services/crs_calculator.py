from dataclasses import dataclass
from datetime import date
from uuid import UUID, uuid4
import logging

from src.modules.crs.infrastructure.repositories.crs_repository_impl import CRSRepositoryImpl

logger = logging.getLogger(__name__)

FORMULA_VERSION = "v1.0"

# Weights with history
W_PRIORITIES = 0.40
W_TASKS = 0.30
W_CONSISTENCY = 0.20
W_CARRYOVER = 0.10

# Weights without history (re-ponder: divide by 0.80)
W_PRIORITIES_NO_HIST = 0.50
W_TASKS_NO_HIST = 0.375
W_CARRYOVER_NO_HIST = 0.125


@dataclass
class CRSResult:
    score: float
    trend: str
    risk_level: str
    formula_version: str


class CRSCalculationService:
    def __init__(self, crs_repo: CRSRepositoryImpl) -> None:
        self._crs_repo = crs_repo

    async def calculate(
        self,
        employee_id: UUID,
        organization_id: UUID,
        checkout_id: UUID,
        week_start: date,
        priorities_total: int,
        priorities_completed: int,
        priorities_carried: int,
        tasks_total: int,
        tasks_completed: int,
    ) -> CRSResult:
        # Component 1: Priority completion
        comp_priorities = (priorities_completed / priorities_total * 100) if priorities_total > 0 else 100.0

        # Component 2: Task completion
        comp_tasks = (tasks_completed / tasks_total * 100) if tasks_total > 0 else 100.0

        # Component 4: Carryover penalty
        comp_carryover = ((1 - priorities_carried / priorities_total) * 100) if priorities_total > 0 else 100.0

        # Component 3: Historical consistency
        historical_scores = await self._crs_repo.get_last_n_scores(employee_id, organization_id, 4)

        if historical_scores:
            comp_consistency = sum(historical_scores) / len(historical_scores)
            score = (
                W_PRIORITIES * comp_priorities
                + W_TASKS * comp_tasks
                + W_CONSISTENCY * comp_consistency
                + W_CARRYOVER * comp_carryover
            )
        else:
            # First week: re-ponder without consistency
            score = (
                W_PRIORITIES_NO_HIST * comp_priorities
                + W_TASKS_NO_HIST * comp_tasks
                + W_CARRYOVER_NO_HIST * comp_carryover
            )

        # Clamp 0-100
        score = max(0.0, min(100.0, score))

        # Trend
        if not historical_scores:
            trend = "stable"
        else:
            avg = sum(historical_scores) / len(historical_scores)
            diff = score - avg
            if diff > 5:
                trend = "improving"
            elif diff < -5:
                trend = "declining"
            else:
                trend = "stable"

        # Risk level
        if score >= 75:
            risk_level = "low"
        elif score >= 60:
            risk_level = "moderate"
        else:
            risk_level = "high"

        # Persist
        crs_id = uuid4()
        await self._crs_repo.save(
            crs_id=crs_id,
            organization_id=organization_id,
            employee_id=employee_id,
            checkout_id=checkout_id,
            week_start=week_start,
            score=round(score, 2),
            trend=trend,
            risk_level=risk_level,
            formula_version=FORMULA_VERSION,
            priorities_total=priorities_total,
            priorities_completed=priorities_completed,
            tasks_total=tasks_total,
            tasks_completed=tasks_completed,
        )

        logger.info("CRS calculated: employee=%s week=%s score=%.2f trend=%s risk=%s",
                    employee_id, week_start, score, trend, risk_level)

        return CRSResult(score=round(score, 2), trend=trend, risk_level=risk_level, formula_version=FORMULA_VERSION)
