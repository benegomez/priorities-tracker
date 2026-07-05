from datetime import date
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pytest

from src.modules.checkin.application.commands.create_checkin import CreateCheckInCommand, CreateCheckInUseCase
from src.modules.checkin.application.commands.submit_checkin import SubmitCheckInCommand, SubmitCheckInUseCase
from src.modules.checkin.domain.entities.checkin import WeeklyCheckIn
from src.shared.exceptions.base import BusinessRuleViolation, ValidationException


@pytest.fixture
def mock_checkin_repo():
    return AsyncMock()


@pytest.fixture
def mock_priority_repo():
    return AsyncMock()


class TestCreateCheckIn:
    @pytest.mark.asyncio
    async def test_create_checkin_returns_draft_status(self, mock_checkin_repo):
        mock_checkin_repo.get_by_employee_and_week.return_value = None
        use_case = CreateCheckInUseCase(checkin_repo=mock_checkin_repo)

        result = await use_case.execute(CreateCheckInCommand(
            employee_id=uuid4(), organization_id=uuid4(), week_start=date(2025, 1, 6)
        ))

        assert result.status == "draft"
        mock_checkin_repo.save.assert_called_once()

    @pytest.mark.asyncio
    async def test_create_checkin_raises_br001_when_duplicate_week(self, mock_checkin_repo):
        mock_checkin_repo.get_by_employee_and_week.return_value = MagicMock()
        use_case = CreateCheckInUseCase(checkin_repo=mock_checkin_repo)

        with pytest.raises(BusinessRuleViolation, match="BR-001"):
            await use_case.execute(CreateCheckInCommand(
                employee_id=uuid4(), organization_id=uuid4(), week_start=date(2025, 1, 6)
            ))

    @pytest.mark.asyncio
    async def test_create_checkin_validates_week_start_is_monday(self, mock_checkin_repo):
        mock_checkin_repo.get_by_employee_and_week.return_value = None
        use_case = CreateCheckInUseCase(checkin_repo=mock_checkin_repo)

        with pytest.raises(ValidationException, match="Monday"):
            await use_case.execute(CreateCheckInCommand(
                employee_id=uuid4(), organization_id=uuid4(), week_start=date(2025, 1, 7)  # Tuesday
            ))

    @pytest.mark.asyncio
    async def test_create_checkin_extracts_org_id_from_token(self, mock_checkin_repo):
        mock_checkin_repo.get_by_employee_and_week.return_value = None
        org_id = uuid4()
        use_case = CreateCheckInUseCase(checkin_repo=mock_checkin_repo)

        result = await use_case.execute(CreateCheckInCommand(
            employee_id=uuid4(), organization_id=org_id, week_start=date(2025, 1, 6)
        ))

        assert result.organization_id == org_id


class TestSubmitCheckIn:
    @pytest.mark.asyncio
    async def test_submit_checkin_transitions_to_submitted(self, mock_checkin_repo, mock_priority_repo):
        checkin = WeeklyCheckIn(id=uuid4(), organization_id=uuid4(), employee_id=uuid4(), week_start=date(2025, 1, 6))
        mock_checkin_repo.get_by_id.return_value = checkin
        mock_priority_repo.count_by_checkin.return_value = 2
        use_case = SubmitCheckInUseCase(checkin_repo=mock_checkin_repo, priority_repo=mock_priority_repo)

        result = await use_case.execute(SubmitCheckInCommand(
            checkin_id=checkin.id, employee_id=checkin.employee_id, organization_id=checkin.organization_id
        ))

        assert result.status == "submitted"
        assert result.submitted_at is not None

    @pytest.mark.asyncio
    async def test_submit_checkin_raises_409_when_no_priorities(self, mock_checkin_repo, mock_priority_repo):
        checkin = WeeklyCheckIn(id=uuid4(), organization_id=uuid4(), employee_id=uuid4(), week_start=date(2025, 1, 6))
        mock_checkin_repo.get_by_id.return_value = checkin
        mock_priority_repo.count_by_checkin.return_value = 0
        use_case = SubmitCheckInUseCase(checkin_repo=mock_checkin_repo, priority_repo=mock_priority_repo)

        with pytest.raises(BusinessRuleViolation, match="at least one priority"):
            await use_case.execute(SubmitCheckInCommand(
                checkin_id=checkin.id, employee_id=checkin.employee_id, organization_id=checkin.organization_id
            ))

    @pytest.mark.asyncio
    async def test_submit_checkin_raises_409_when_already_submitted(self, mock_checkin_repo, mock_priority_repo):
        checkin = WeeklyCheckIn(id=uuid4(), organization_id=uuid4(), employee_id=uuid4(), week_start=date(2025, 1, 6), status="submitted")
        mock_checkin_repo.get_by_id.return_value = checkin
        mock_priority_repo.count_by_checkin.return_value = 1
        use_case = SubmitCheckInUseCase(checkin_repo=mock_checkin_repo, priority_repo=mock_priority_repo)

        with pytest.raises(BusinessRuleViolation):
            await use_case.execute(SubmitCheckInCommand(
                checkin_id=checkin.id, employee_id=checkin.employee_id, organization_id=checkin.organization_id
            ))

    @pytest.mark.asyncio
    async def test_submit_checkin_transitions_priorities_to_planned(self, mock_checkin_repo, mock_priority_repo):
        checkin = WeeklyCheckIn(id=uuid4(), organization_id=uuid4(), employee_id=uuid4(), week_start=date(2025, 1, 6))
        mock_checkin_repo.get_by_id.return_value = checkin
        mock_priority_repo.count_by_checkin.return_value = 1
        use_case = SubmitCheckInUseCase(checkin_repo=mock_checkin_repo, priority_repo=mock_priority_repo)

        await use_case.execute(SubmitCheckInCommand(
            checkin_id=checkin.id, employee_id=checkin.employee_id, organization_id=checkin.organization_id
        ))

        mock_priority_repo.transition_to_planned.assert_called_once_with(
            checkin_id=checkin.id, organization_id=checkin.organization_id
        )
