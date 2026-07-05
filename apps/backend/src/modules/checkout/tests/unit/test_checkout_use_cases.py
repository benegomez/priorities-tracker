import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4
from datetime import date

from src.modules.checkout.domain.entities.checkout import WeeklyCheckOut
from src.modules.checkout.application.commands.create_checkout import CreateCheckOutCommand, CreateCheckOutUseCase
from src.modules.checkout.application.commands.submit_checkout import SubmitCheckOutCommand, SubmitCheckOutUseCase
from src.shared.exceptions.base import AuthorizationException, BusinessRuleViolation


ORG_ID = uuid4()
EMP_ID = uuid4()
CHECKIN_ID = uuid4()
CHECKOUT_ID = uuid4()
WEEK = date(2026, 6, 29)


class TestCreateCheckOut:
    @pytest.mark.asyncio
    async def test_create_checkout_returns_draft(self):
        mock_repo = AsyncMock()
        mock_repo.get_by_employee_and_week.return_value = None
        mock_repo.save.return_value = None

        mock_session = AsyncMock()
        checkin_row = MagicMock(id=CHECKIN_ID, employee_id=EMP_ID, organization_id=ORG_ID, week_start=WEEK, status="submitted")
        mock_session.execute.return_value = MagicMock(one_or_none=MagicMock(return_value=checkin_row))

        use_case = CreateCheckOutUseCase(checkout_repo=mock_repo, session=mock_session)
        result = await use_case.execute(CreateCheckOutCommand(checkin_id=CHECKIN_ID, employee_id=EMP_ID, organization_id=ORG_ID))

        assert result.status == "draft"
        assert result.checkin_id == CHECKIN_ID
        mock_repo.save.assert_called_once()

    @pytest.mark.asyncio
    async def test_create_checkout_raises_br002_when_duplicate(self):
        mock_repo = AsyncMock()
        existing = WeeklyCheckOut(id=uuid4(), organization_id=ORG_ID, employee_id=EMP_ID, checkin_id=CHECKIN_ID, week_start=WEEK)
        mock_repo.get_by_employee_and_week.return_value = existing

        mock_session = AsyncMock()
        checkin_row = MagicMock(id=CHECKIN_ID, employee_id=EMP_ID, organization_id=ORG_ID, week_start=WEEK, status="submitted")
        mock_session.execute.return_value = MagicMock(one_or_none=MagicMock(return_value=checkin_row))

        use_case = CreateCheckOutUseCase(checkout_repo=mock_repo, session=mock_session)
        with pytest.raises(BusinessRuleViolation, match="BR-002"):
            await use_case.execute(CreateCheckOutCommand(checkin_id=CHECKIN_ID, employee_id=EMP_ID, organization_id=ORG_ID))

    @pytest.mark.asyncio
    async def test_create_checkout_raises_when_checkin_not_submitted(self):
        mock_repo = AsyncMock()
        mock_session = AsyncMock()
        checkin_row = MagicMock(id=CHECKIN_ID, employee_id=EMP_ID, organization_id=ORG_ID, week_start=WEEK, status="draft")
        mock_session.execute.return_value = MagicMock(one_or_none=MagicMock(return_value=checkin_row))

        use_case = CreateCheckOutUseCase(checkout_repo=mock_repo, session=mock_session)
        with pytest.raises(BusinessRuleViolation, match="submitted"):
            await use_case.execute(CreateCheckOutCommand(checkin_id=CHECKIN_ID, employee_id=EMP_ID, organization_id=ORG_ID))

    @pytest.mark.asyncio
    async def test_create_checkout_raises_403_when_wrong_employee(self):
        mock_repo = AsyncMock()
        mock_session = AsyncMock()
        other_emp = uuid4()
        checkin_row = MagicMock(id=CHECKIN_ID, employee_id=other_emp, organization_id=ORG_ID, week_start=WEEK, status="submitted")
        mock_session.execute.return_value = MagicMock(one_or_none=MagicMock(return_value=checkin_row))

        use_case = CreateCheckOutUseCase(checkout_repo=mock_repo, session=mock_session)
        with pytest.raises(AuthorizationException, match="BR-013"):
            await use_case.execute(CreateCheckOutCommand(checkin_id=CHECKIN_ID, employee_id=EMP_ID, organization_id=ORG_ID))


class TestSubmitCheckOut:
    def _make_checkout(self, status="draft"):
        return WeeklyCheckOut(id=CHECKOUT_ID, organization_id=ORG_ID, employee_id=EMP_ID, checkin_id=CHECKIN_ID, week_start=WEEK, status=status)

    @pytest.mark.asyncio
    async def test_submit_transitions_to_submitted(self):
        mock_repo = AsyncMock()
        mock_repo.get_by_id.return_value = self._make_checkout()
        mock_repo.update.return_value = None

        mock_session = AsyncMock()
        # Mock priority/task counts
        p_row = MagicMock(total=3, completed=2, carried=1)
        t_row = MagicMock(total=5, completed=4)
        mock_session.execute.side_effect = [
            MagicMock(),  # update priorities completed
            MagicMock(),  # update priorities carried_over
            MagicMock(),  # update tasks completed
            MagicMock(),  # update tasks cancelled
            MagicMock(one=MagicMock(return_value=p_row)),  # priority summary
            MagicMock(one=MagicMock(return_value=t_row)),  # task summary
        ]

        use_case = SubmitCheckOutUseCase(checkout_repo=mock_repo, session=mock_session)
        checkout, summary = await use_case.execute(
            SubmitCheckOutCommand(checkout_id=CHECKOUT_ID, employee_id=EMP_ID, organization_id=ORG_ID, notes="Done")
        )

        assert checkout.status == "submitted"
        assert checkout.notes == "Done"
        assert summary.priorities_total == 3
        assert summary.priorities_completed == 2
        assert summary.priorities_carried == 1
        assert summary.tasks_total == 5
        assert summary.tasks_completed == 4

    @pytest.mark.asyncio
    async def test_submit_raises_409_when_already_submitted(self):
        mock_repo = AsyncMock()
        mock_repo.get_by_id.return_value = self._make_checkout(status="submitted")
        mock_session = AsyncMock()

        use_case = SubmitCheckOutUseCase(checkout_repo=mock_repo, session=mock_session)
        with pytest.raises(BusinessRuleViolation, match="draft"):
            await use_case.execute(
                SubmitCheckOutCommand(checkout_id=CHECKOUT_ID, employee_id=EMP_ID, organization_id=ORG_ID)
            )

    @pytest.mark.asyncio
    async def test_submit_raises_403_when_wrong_employee(self):
        mock_repo = AsyncMock()
        mock_repo.get_by_id.return_value = self._make_checkout()
        mock_session = AsyncMock()

        use_case = SubmitCheckOutUseCase(checkout_repo=mock_repo, session=mock_session)
        with pytest.raises(AuthorizationException, match="BR-013"):
            await use_case.execute(
                SubmitCheckOutCommand(checkout_id=CHECKOUT_ID, employee_id=uuid4(), organization_id=ORG_ID)
            )
