"""Integration tests for reporting endpoints (US-017)."""
import pytest
import httpx
from uuid import uuid4

BASE_URL = "http://localhost:8000"
BASE = "/api/v1/reports"

_TOKEN_CACHE: dict[str, str] = {}


async def _get_token(email: str, password: str) -> str:
    if email not in _TOKEN_CACHE:
        async with httpx.AsyncClient(base_url=BASE_URL, timeout=10) as c:
            r = await c.post("/api/v1/auth/login", json={"email": email, "password": password})
            _TOKEN_CACHE[email] = r.json()["access_token"]
    return _TOKEN_CACHE[email]


async def _employee_headers() -> dict:
    return {"Authorization": f"Bearer {await _get_token('employee@org-alpha.com', 'Employee1234!')}"}


async def _manager_headers() -> dict:
    return {"Authorization": f"Bearer {await _get_token('manager@org-alpha.com', 'Manager1234!')}"}


async def _admin_headers() -> dict:
    return {"Authorization": f"Bearer {await _get_token('admin@org-alpha.com', 'Admin1234!')}"}


async def _get_any_project_id() -> str | None:
    async with httpx.AsyncClient(base_url=BASE_URL, timeout=10) as c:
        r = await c.get("/api/v1/projects", headers=await _admin_headers())
        items = r.json().get("items", [])
        return items[0]["id"] if items else None


@pytest.mark.asyncio
class TestIndividualReport:
    async def test_individual_report_returns_breakdown(self):
        async with httpx.AsyncClient(base_url=BASE_URL, timeout=10) as c:
            r = await c.get(f"{BASE}/individual", headers=await _employee_headers())
        assert r.status_code == 200
        data = r.json()
        assert "employee" in data
        assert "weekly_breakdown" in data
        assert "total_priorities" in data
        assert "completion_rate" in data
        assert isinstance(data["weekly_breakdown"], list)

    async def test_individual_report_employee_can_access(self):
        async with httpx.AsyncClient(base_url=BASE_URL, timeout=10) as c:
            r = await c.get(f"{BASE}/individual", headers=await _employee_headers())
        assert r.status_code == 200

    async def test_individual_report_weeks_param(self):
        async with httpx.AsyncClient(base_url=BASE_URL, timeout=10) as c:
            r = await c.get(f"{BASE}/individual?weeks=4", headers=await _employee_headers())
        assert r.status_code == 200
        assert r.json()["period_weeks"] == 4


@pytest.mark.asyncio
class TestTeamReport:
    async def test_team_report_returns_members(self):
        async with httpx.AsyncClient(base_url=BASE_URL, timeout=10) as c:
            r = await c.get(f"{BASE}/team", headers=await _manager_headers())
        assert r.status_code == 200
        data = r.json()
        assert "members" in data
        assert "team_size" in data
        assert "avg_completion_rate" in data
        assert "weekly_breakdown" in data
        assert isinstance(data["members"], list)

    async def test_team_report_employee_gets_403(self):
        async with httpx.AsyncClient(base_url=BASE_URL, timeout=10) as c:
            r = await c.get(f"{BASE}/team", headers=await _employee_headers())
        assert r.status_code == 403


@pytest.mark.asyncio
class TestProjectReport:
    async def test_project_report_returns_phases(self):
        project_id = await _get_any_project_id()
        if not project_id:
            pytest.skip("No projects available in seed data")
        async with httpx.AsyncClient(base_url=BASE_URL, timeout=10) as c:
            r = await c.get(f"{BASE}/project/{project_id}", headers=await _manager_headers())
        assert r.status_code == 200
        data = r.json()
        assert "project" in data
        assert "phases" in data
        assert "total_priorities" in data
        assert "completion_rate" in data
        assert isinstance(data["phases"], list)

    async def test_project_report_unknown_project_returns_404(self):
        async with httpx.AsyncClient(base_url=BASE_URL, timeout=10) as c:
            r = await c.get(f"{BASE}/project/{uuid4()}", headers=await _manager_headers())
        assert r.status_code == 404
