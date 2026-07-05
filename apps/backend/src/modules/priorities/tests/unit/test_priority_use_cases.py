from datetime import date
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4

import pytest

from src.modules.checkin.domain.entities.checkin import WeeklyCheckIn
from src.modules.priorities.application.commands.create_priority import CreatePriorityCommand, CreatePriorityUseCase
from src.modules.priorities.application.commands.create_task import CreateTaskCommand, CreateTaskUseCase
from src.modules.priorities.domain.entities.priority import Priority
from src.shared.exceptions.base import AuthorizationException, BusinessRuleViolation


@pytest.fixture
def mock_priority_repo():
    return AsyncMock()


@pytest.fixture
def mock_task_repo():
    return AsyncMock()


@pytest.fixture
def mock_checkin_repo():
    return AsyncMock()


@pytest.fixture
def mock_session():
    session = AsyncMock()
    return session


class TestCreatePriority:
    @pytest.mark.asyncio
    async def test_create_priority_returns_draft_status(self, mock_priority_repo, mock_checkin_repo, mock_session):
        employee_id = uuid4()
        org_id = uuid4()
        checkin = WeeklyCheckIn(id=uuid4(), organization_id=org_id, employee_id=employee_id, week_start=date(2025, 1, 6))
        mock_checkin_repo.get_by_id.return_value = checkin

        result_row = MagicMock()
        result_row.project_status = "active"
        mock_result = MagicMock()
        mock_result.one_or_none.return_value = result_row
        mock_session.execute.return_value = mock_result

        use_case = CreatePriorityUseCase(priority_repo=mock_priority_repo, checkin_repo=mock_checkin_repo, session=mock_session)
        result = await use_case.execute(CreatePriorityCommand(
            checkin_id=checkin.id, phase_id=uuid4(), title="Test priority",
            description=None, priority_level="high", employee_id=employee_id, organization_id=org_id,
        ))

        assert result.status == "draft"
        mock_priority_repo.save.assert_called_once()

    @pytest.mark.asyncio
    async def test_create_priority_raises_when_checkin_closed(self, mock_priority_repo, mock_checkin_repo, mock_session):
        employee_id = uuid4()
        org_id = uuid4()
        checkin = WeeklyCheckIn(id=uuid4(), organization_id=org_id, employee_id=employee_id, week_start=date(2025, 1, 6), status="closed")
        mock_checkin_repo.get_by_id.return_value = checkin

        use_case = CreatePriorityUseCase(priority_repo=mock_priority_repo, checkin_repo=mock_checkin_repo, session=mock_session)

        with pytest.raises(BusinessRuleViolation, match="closed"):
            await use_case.execute(CreatePriorityCommand(
                checkin_id=checkin.id, phase_id=uuid4(), title="Test",
                description=None, priority_level="high", employee_id=employee_id, organization_id=org_id,
            ))

    @pytest.mark.asyncio
    async def test_create_priority_allows_submitted_checkin(self, mock_priority_repo, mock_checkin_repo, mock_session):
        employee_id = uuid4()
        org_id = uuid4()
        checkin = WeeklyCheckIn(id=uuid4(), organization_id=org_id, employee_id=employee_id, week_start=date(2025, 1, 6), status="submitted")
        mock_checkin_repo.get_by_id.return_value = checkin

        # Mock: no checkout exists
        checkout_result = MagicMock()
        checkout_result.one_or_none.return_value = None
        # Mock: phase validation
        phase_result = MagicMock()
        phase_result.one_or_none.return_value = MagicMock(project_status="active")
        mock_session.execute.side_effect = [checkout_result, phase_result]

        use_case = CreatePriorityUseCase(priority_repo=mock_priority_repo, checkin_repo=mock_checkin_repo, session=mock_session)
        result = await use_case.execute(CreatePriorityCommand(
            checkin_id=checkin.id, phase_id=uuid4(), title="New priority",
            description=None, priority_level="medium", employee_id=employee_id, organization_id=org_id,
        ))

        assert result.status == "draft"
        mock_priority_repo.save.assert_called_once()

    @pytest.mark.asyncio
    async def test_create_priority_raises_409_when_checkout_exists(self, mock_priority_repo, mock_checkin_repo, mock_session):
        employee_id = uuid4()
        org_id = uuid4()
        checkin = WeeklyCheckIn(id=uuid4(), organization_id=org_id, employee_id=employee_id, week_start=date(2025, 1, 6), status="submitted")
        mock_checkin_repo.get_by_id.return_value = checkin

        # Mock: checkout exists
        checkout_result = MagicMock()
        checkout_result.one_or_none.return_value = MagicMock(id=uuid4())
        mock_session.execute.return_value = checkout_result

        use_case = CreatePriorityUseCase(priority_repo=mock_priority_repo, checkin_repo=mock_checkin_repo, session=mock_session)

        with pytest.raises(BusinessRuleViolation, match="locked"):
            await use_case.execute(CreatePriorityCommand(
                checkin_id=checkin.id, phase_id=uuid4(), title="Test",
                description=None, priority_level="high", employee_id=employee_id, organization_id=org_id,
            ))

    @pytest.mark.asyncio
    async def test_create_priority_raises_br004_when_project_inactive(self, mock_priority_repo, mock_checkin_repo, mock_session):
        employee_id = uuid4()
        org_id = uuid4()
        checkin = WeeklyCheckIn(id=uuid4(), organization_id=org_id, employee_id=employee_id, week_start=date(2025, 1, 6))
        mock_checkin_repo.get_by_id.return_value = checkin

        result_row = MagicMock()
        result_row.project_status = "draft"
        mock_result = MagicMock()
        mock_result.one_or_none.return_value = result_row
        mock_session.execute.return_value = mock_result

        use_case = CreatePriorityUseCase(priority_repo=mock_priority_repo, checkin_repo=mock_checkin_repo, session=mock_session)

        with pytest.raises(BusinessRuleViolation, match="BR-004"):
            await use_case.execute(CreatePriorityCommand(
                checkin_id=checkin.id, phase_id=uuid4(), title="Test",
                description=None, priority_level="high", employee_id=employee_id, organization_id=org_id,
            ))

    @pytest.mark.asyncio
    async def test_create_priority_raises_br013_when_wrong_employee(self, mock_priority_repo, mock_checkin_repo, mock_session):
        org_id = uuid4()
        checkin = WeeklyCheckIn(id=uuid4(), organization_id=org_id, employee_id=uuid4(), week_start=date(2025, 1, 6))
        mock_checkin_repo.get_by_id.return_value = checkin

        use_case = CreatePriorityUseCase(priority_repo=mock_priority_repo, checkin_repo=mock_checkin_repo, session=mock_session)

        with pytest.raises(AuthorizationException, match="BR-013"):
            await use_case.execute(CreatePriorityCommand(
                checkin_id=checkin.id, phase_id=uuid4(), title="Test",
                description=None, priority_level="high", employee_id=uuid4(), organization_id=org_id,
            ))

    @pytest.mark.asyncio
    async def test_create_priority_raises_br016_when_cross_tenant(self, mock_priority_repo, mock_checkin_repo, mock_session):
        employee_id = uuid4()
        org_id = uuid4()
        checkin = WeeklyCheckIn(id=uuid4(), organization_id=org_id, employee_id=employee_id, week_start=date(2025, 1, 6))
        mock_checkin_repo.get_by_id.return_value = checkin

        mock_result = MagicMock()
        mock_result.one_or_none.return_value = None
        mock_session.execute.return_value = mock_result

        use_case = CreatePriorityUseCase(priority_repo=mock_priority_repo, checkin_repo=mock_checkin_repo, session=mock_session)

        with pytest.raises(AuthorizationException, match="BR-016"):
            await use_case.execute(CreatePriorityCommand(
                checkin_id=checkin.id, phase_id=uuid4(), title="Test",
                description=None, priority_level="high", employee_id=employee_id, organization_id=org_id,
            ))


class TestCreateTask:
    @pytest.mark.asyncio
    async def test_create_task_returns_pending_status(self, mock_task_repo, mock_priority_repo):
        employee_id = uuid4()
        org_id = uuid4()
        priority = Priority(
            id=uuid4(), organization_id=org_id, checkin_id=uuid4(), phase_id=uuid4(),
            owner_id=employee_id, week_start=date(2025, 1, 6), title="Test priority",
        )
        mock_priority_repo.get_by_id.return_value = priority

        use_case = CreateTaskUseCase(task_repo=mock_task_repo, priority_repo=mock_priority_repo)
        result = await use_case.execute(CreateTaskCommand(
            priority_id=priority.id, title="Test task", description=None,
            employee_id=employee_id, organization_id=org_id,
        ))

        assert result.status == "pending"
        mock_task_repo.save.assert_called_once()

    @pytest.mark.asyncio
    async def test_create_task_raises_br005_when_no_priority(self, mock_task_repo, mock_priority_repo):
        mock_priority_repo.get_by_id.return_value = None

        use_case = CreateTaskUseCase(task_repo=mock_task_repo, priority_repo=mock_priority_repo)

        with pytest.raises(BusinessRuleViolation, match="BR-005"):
            await use_case.execute(CreateTaskCommand(
                priority_id=uuid4(), title="Test task", description=None,
                employee_id=uuid4(), organization_id=uuid4(),
            ))

    @pytest.mark.asyncio
    async def test_create_task_raises_when_priority_not_owned(self, mock_task_repo, mock_priority_repo):
        org_id = uuid4()
        priority = Priority(
            id=uuid4(), organization_id=org_id, checkin_id=uuid4(), phase_id=uuid4(),
            owner_id=uuid4(), week_start=date(2025, 1, 6), title="Test priority",
        )
        mock_priority_repo.get_by_id.return_value = priority

        use_case = CreateTaskUseCase(task_repo=mock_task_repo, priority_repo=mock_priority_repo)

        with pytest.raises(AuthorizationException, match="BR-013"):
            await use_case.execute(CreateTaskCommand(
                priority_id=priority.id, title="Test task", description=None,
                employee_id=uuid4(), organization_id=org_id,
            ))
