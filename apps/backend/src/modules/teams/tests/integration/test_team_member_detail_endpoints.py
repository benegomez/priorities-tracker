"""Integration tests for manager individual view endpoints (US-016)."""
import pytest
import httpx
from uuid import uuid4

BASE_URL = "http://localhost:8000"
BASE = "/api/v1/teams"

_TOKEN_CACHE: dict[str, str] = {}


async def _get_token(email: str, password: str) -> str:
    if email not in _TOKEN_CACHE:
        async with httpx.AsyncClient(base_url=BASE_URL, timeout=10) as c:
            r = await c.post("/api/v1/auth/login", json={"email": email, "password": password})
            _TOKEN_CACHE[email] = r.json()["access_token"]
    return _TOKEN_CACHE[email]


async def _manager_headers() -> dict:
    return {"Authorization": f"Bearer {await _get_token('manager@org-alpha.com', 'Manager1234!')}"}


async def _employee_headers() -> dict:
    return {"Authorization": f"Bearer {await _get_token('employee@org-alpha.com', 'Employee1234!')}"}


async def _admin_headers() -> dict:
    return {"Authorization": f"Bearer {await _get_token('admin@org-alpha.com', 'Admin1234!')}"}


async def _get_direct_report_id() -> str | None:
    """Returns the first direct report of the seeded manager, or None."""
    async with httpx.AsyncClient(base_url=BASE_URL, timeout=10) as c:
        r = await c.get(f"{BASE}/my-team", headers=await _manager_headers())
        members = r.json().get("members", [])
        return members[0]["id"] if members else None


@pytest.mark.asyncio
class TestGetMemberCRS:
    async def test_get_member_crs_returns_current_and_history(self):
        employee_id = await _get_direct_report_id()
        if not employee_id:
            pytest.skip("Manager has no direct reports in seed data")
        async with httpx.AsyncClient(base_url=BASE_URL, timeout=10) as c:
            r = await c.get(
                f"{BASE}/my-team/{employee_id}/crs",
                headers=await _manager_headers(),
            )
        assert r.status_code == 200
        data = r.json()
        assert "employee" in data
        assert "current" in data
        assert "history" in data
        assert isinstance(data["history"], list)
        employee = data["employee"]
        assert "id" in employee
        assert "first_name" in employee
        assert "last_name" in employee

    async def test_get_member_crs_employee_gets_403(self):
        employee_id = await _get_direct_report_id()
        if not employee_id:
            pytest.skip("Manager has no direct reports in seed data")
        async with httpx.AsyncClient(base_url=BASE_URL, timeout=10) as c:
            r = await c.get(
                f"{BASE}/my-team/{employee_id}/crs",
                headers=await _employee_headers(),
            )
        assert r.status_code == 403

    async def test_get_member_crs_403_for_non_direct_report(self):
        random_id = str(uuid4())
        async with httpx.AsyncClient(base_url=BASE_URL, timeout=10) as c:
            r = await c.get(
                f"{BASE}/my-team/{random_id}/crs",
                headers=await _manager_headers(),
            )
        assert r.status_code == 403

    async def test_get_member_crs_weeks_param_limits_history(self):
        employee_id = await _get_direct_report_id()
        if not employee_id:
            pytest.skip("Manager has no direct reports in seed data")
        async with httpx.AsyncClient(base_url=BASE_URL, timeout=10) as c:
            r = await c.get(
                f"{BASE}/my-team/{employee_id}/crs?weeks=2",
                headers=await _manager_headers(),
            )
        assert r.status_code == 200
        assert len(r.json()["history"]) <= 2

    async def test_get_member_crs_no_crs_returns_null_current(self):
        """A new employee with no CRS calculated returns current: null and history: []."""
        admin_h = await _admin_headers()
        new_email = f"emp_{uuid4().hex[:6]}@org-alpha.com"
        async with httpx.AsyncClient(base_url=BASE_URL, timeout=10) as c:
            # Create a new manager with no team
            mgr_r = await c.post(
                "/api/v1/users",
                json={"email": f"mgr_{uuid4().hex[:6]}@org-alpha.com", "first_name": "Temp", "last_name": "Mgr", "role": "manager"},
                headers=admin_h,
            )
            if mgr_r.status_code not in (200, 201):
                pytest.skip("Cannot create temp manager")
            mgr_temp_pw = mgr_r.json().get("temporary_password")

            # Create a new employee with no CRS
            emp_r = await c.post(
                "/api/v1/users",
                json={"email": new_email, "first_name": "New", "last_name": "Emp", "role": "employee"},
                headers=admin_h,
            )
            if emp_r.status_code not in (200, 201):
                pytest.skip("Cannot create temp employee")
            emp_id = emp_r.json()["id"]

            # Create a team, assign manager and employee
            team_r = await c.post(
                "/api/v1/teams",
                json={"name": f"TmpTeam {uuid4().hex[:6]}"},
                headers=admin_h,
            )
            if team_r.status_code not in (200, 201):
                pytest.skip("Cannot create temp team")
            team_id = team_r.json()["id"]

            await c.post(f"/api/v1/teams/{team_id}/members", json={"user_id": emp_id}, headers=admin_h)

            # Assign manager to employee
            mgr_id = mgr_r.json()["id"]
            await c.patch(f"/api/v1/users/{emp_id}", json={"manager_id": mgr_id}, headers=admin_h)

            # Login as temp manager
            if not mgr_temp_pw:
                pytest.skip("No temporary_password returned")
            token_r = await c.post("/api/v1/auth/login", json={"email": mgr_r.json()["email"], "password": mgr_temp_pw})
            if token_r.status_code != 200:
                pytest.skip("Cannot login as temp manager")
            mgr_token = token_r.json()["access_token"]

            r = await c.get(
                f"{BASE}/my-team/{emp_id}/crs",
                headers={"Authorization": f"Bearer {mgr_token}"},
            )

        assert r.status_code == 200
        data = r.json()
        assert data["current"] is None
        assert data["history"] == []


@pytest.mark.asyncio
class TestGetMemberCheckinByWeek:
    async def test_get_checkin_with_week_start_returns_correct_week(self):
        """GET /my-team/{id}/checkin?week_start=YYYY-MM-DD returns check-in for that week."""
        employee_id = await _get_direct_report_id()
        if not employee_id:
            pytest.skip("Manager has no direct reports in seed data")
        # Fetch CRS history to get a known week_start with data
        async with httpx.AsyncClient(base_url=BASE_URL, timeout=10) as c:
            crs_r = await c.get(
                f"{BASE}/my-team/{employee_id}/crs?weeks=8",
                headers=await _manager_headers(),
            )
        history = crs_r.json().get("history", [])
        if not history:
            pytest.skip("No CRS history available to derive a week_start")
        week_start = history[0]["week_start"]

        async with httpx.AsyncClient(base_url=BASE_URL, timeout=10) as c:
            r = await c.get(
                f"{BASE}/my-team/{employee_id}/checkin?week_start={week_start}",
                headers=await _manager_headers(),
            )
        assert r.status_code in (200, 404)  # 200 if check-in exists, 404 if not
        if r.status_code == 200:
            data = r.json()
            assert data["week_start"] == week_start
            assert "priorities" in data

    async def test_get_checkin_nonexistent_week_returns_404(self):
        """GET /my-team/{id}/checkin?week_start for a week with no check-in returns 404."""
        employee_id = await _get_direct_report_id()
        if not employee_id:
            pytest.skip("Manager has no direct reports in seed data")
        async with httpx.AsyncClient(base_url=BASE_URL, timeout=10) as c:
            r = await c.get(
                f"{BASE}/my-team/{employee_id}/checkin?week_start=2020-01-06",
                headers=await _manager_headers(),
            )
        assert r.status_code == 404

    async def test_get_checkin_with_week_start_non_direct_report_returns_403(self):
        """week_start param does not bypass the direct-report validation."""
        random_id = str(uuid4())
        async with httpx.AsyncClient(base_url=BASE_URL, timeout=10) as c:
            r = await c.get(
                f"{BASE}/my-team/{random_id}/checkin?week_start=2025-06-30",
                headers=await _manager_headers(),
            )
        assert r.status_code == 403
