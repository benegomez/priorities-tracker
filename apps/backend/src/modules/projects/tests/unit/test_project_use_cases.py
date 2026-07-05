import pytest
from uuid import uuid4

from src.modules.projects.domain.entities.project import Project, VALID_PROJECT_TRANSITIONS
from src.modules.projects.domain.entities.phase import ProjectPhase, VALID_PHASE_TRANSITIONS
from src.shared.exceptions.base import BusinessRuleViolation


ORG_ID = uuid4()


class TestProjectStateMachine:
    def test_draft_to_active(self):
        p = Project(id=uuid4(), organization_id=ORG_ID, owner_id=uuid4(), name="Test", status="draft")
        p.change_status("active")
        assert p.status == "active"

    def test_active_to_on_hold(self):
        p = Project(id=uuid4(), organization_id=ORG_ID, owner_id=uuid4(), name="Test", status="active")
        p.change_status("on_hold")
        assert p.status == "on_hold"

    def test_active_to_completed(self):
        p = Project(id=uuid4(), organization_id=ORG_ID, owner_id=uuid4(), name="Test", status="active")
        p.change_status("completed")
        assert p.status == "completed"

    def test_on_hold_to_active(self):
        p = Project(id=uuid4(), organization_id=ORG_ID, owner_id=uuid4(), name="Test", status="on_hold")
        p.change_status("active")
        assert p.status == "active"

    def test_completed_to_archived(self):
        p = Project(id=uuid4(), organization_id=ORG_ID, owner_id=uuid4(), name="Test", status="completed")
        p.change_status("archived")
        assert p.status == "archived"

    def test_draft_to_completed_raises(self):
        p = Project(id=uuid4(), organization_id=ORG_ID, owner_id=uuid4(), name="Test", status="draft")
        with pytest.raises(BusinessRuleViolation, match="Invalid project transition"):
            p.change_status("completed")

    def test_archived_to_anything_raises(self):
        p = Project(id=uuid4(), organization_id=ORG_ID, owner_id=uuid4(), name="Test", status="archived")
        with pytest.raises(BusinessRuleViolation):
            p.change_status("active")


class TestPhaseStateMachine:
    def test_planned_to_active(self):
        ph = ProjectPhase(id=uuid4(), organization_id=ORG_ID, project_id=uuid4(), name="Test", status="planned")
        ph.change_status("active")
        assert ph.status == "active"

    def test_planned_to_cancelled(self):
        ph = ProjectPhase(id=uuid4(), organization_id=ORG_ID, project_id=uuid4(), name="Test", status="planned")
        ph.change_status("cancelled")
        assert ph.status == "cancelled"

    def test_active_to_completed(self):
        ph = ProjectPhase(id=uuid4(), organization_id=ORG_ID, project_id=uuid4(), name="Test", status="active")
        ph.change_status("completed")
        assert ph.status == "completed"

    def test_active_to_cancelled(self):
        ph = ProjectPhase(id=uuid4(), organization_id=ORG_ID, project_id=uuid4(), name="Test", status="active")
        ph.change_status("cancelled")
        assert ph.status == "cancelled"

    def test_planned_to_completed_raises(self):
        ph = ProjectPhase(id=uuid4(), organization_id=ORG_ID, project_id=uuid4(), name="Test", status="planned")
        with pytest.raises(BusinessRuleViolation, match="Invalid phase transition"):
            ph.change_status("completed")

    def test_completed_to_anything_raises(self):
        ph = ProjectPhase(id=uuid4(), organization_id=ORG_ID, project_id=uuid4(), name="Test", status="completed")
        with pytest.raises(BusinessRuleViolation):
            ph.change_status("active")
