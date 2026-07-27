"""Integration tests for admin project management endpoints."""
import pytest
import httpx
from uuid import uuid4

BASE_URL = "http://localhost:8000"
BASE = "/api/v1/projects"

_TOKEN_CACHE: dict[str, str] = {}


async def _get_token(email: str, password: str) -> str:
    if email not in _TOKEN_CACHE:
        async with httpx.AsyncClient(base_url=BASE_URL, timeout=10) as c:
            r = await c.post("/api/v1/auth/login", json={"email": email, "password": password})
            _TOKEN_CACHE[email] = r.json()["access_token"]
    return _TOKEN_CACHE[email]


async def _admin_headers() -> dict:
    return {"Authorization": f"Bearer {await _get_token('admin@org-alpha.com', 'Admin1234!')}"}


async def _employee_headers() -> dict:
    return {"Authorization": f"Bearer {await _get_token('employee@org-alpha.com', 'Employee1234!')}"}


async def _get_admin_user_id() -> str:
    """Returns the admin user id (valid owner within the org)."""
    async with httpx.AsyncClient(base_url=BASE_URL, timeout=10) as c:
        r = await c.get("/api/v1/users?role=administrator", headers=await _admin_headers())
        return r.json()["items"][0]["id"]


async def _get_employee_user_id() -> str:
    async with httpx.AsyncClient(base_url=BASE_URL, timeout=10) as c:
        r = await c.get("/api/v1/users?role=employee&status=active", headers=await _admin_headers())
        items = r.json()["items"]
        if not items:
            pytest.skip("No active employee users available")
        return items[0]["id"]


async def _create_project(name: str | None = None) -> dict:
    owner_id = await _get_admin_user_id()
    project_name = name or f"Project {uuid4().hex[:6]}"
    async with httpx.AsyncClient(base_url=BASE_URL, timeout=10) as c:
        r = await c.post(BASE, json={"name": project_name, "owner_id": owner_id}, headers=await _admin_headers())
    assert r.status_code == 201
    return r.json()


@pytest.mark.asyncio
class TestListProjects:
    async def test_returns_200_with_items(self):
        async with httpx.AsyncClient(base_url=BASE_URL, timeout=10) as c:
            r = await c.get(BASE, headers=await _admin_headers())
        assert r.status_code == 200
        data = r.json()
        assert "items" in data
        assert "total" in data
        assert "page" in data

    async def test_status_filter(self):
        async with httpx.AsyncClient(base_url=BASE_URL, timeout=10) as c:
            r = await c.get(f"{BASE}?status=draft", headers=await _admin_headers())
        assert r.status_code == 200
        for item in r.json()["items"]:
            assert item["status"] == "draft"


@pytest.mark.asyncio
class TestCreateProject:
    async def test_creates_project_returns_201(self):
        owner_id = await _get_admin_user_id()
        name = f"New Project {uuid4().hex[:6]}"
        async with httpx.AsyncClient(base_url=BASE_URL, timeout=10) as c:
            r = await c.post(BASE, json={"name": name, "owner_id": owner_id}, headers=await _admin_headers())
        assert r.status_code == 201
        data = r.json()
        assert data["name"] == name
        assert data["status"] == "draft"
        assert "id" in data

    async def test_invalid_owner_returns_400(self):
        foreign_owner = str(uuid4())
        async with httpx.AsyncClient(base_url=BASE_URL, timeout=10) as c:
            r = await c.post(
                BASE,
                json={"name": f"Bad Owner {uuid4().hex[:6]}", "owner_id": foreign_owner},
                headers=await _admin_headers(),
            )
        assert r.status_code == 400

    async def test_employee_cannot_create_returns_403(self):
        async with httpx.AsyncClient(base_url=BASE_URL, timeout=10) as c:
            r = await c.post(
                BASE,
                json={"name": "Forbidden", "owner_id": str(uuid4())},
                headers=await _employee_headers(),
            )
        assert r.status_code == 403


@pytest.mark.asyncio
class TestGetProjectDetail:
    async def test_returns_detail_with_phases_and_members(self):
        project = await _create_project()
        project_id = project["id"]
        async with httpx.AsyncClient(base_url=BASE_URL, timeout=10) as c:
            r = await c.get(f"{BASE}/{project_id}", headers=await _admin_headers())
        assert r.status_code == 200
        data = r.json()
        assert data["id"] == project_id
        assert "phases" in data
        assert "members" in data

    async def test_unknown_project_returns_404(self):
        async with httpx.AsyncClient(base_url=BASE_URL, timeout=10) as c:
            r = await c.get(f"{BASE}/{uuid4()}", headers=await _admin_headers())
        assert r.status_code == 404


@pytest.mark.asyncio
class TestUpdateProject:
    async def test_valid_transition_draft_to_active(self):
        project = await _create_project()
        project_id = project["id"]
        async with httpx.AsyncClient(base_url=BASE_URL, timeout=10) as c:
            r = await c.patch(f"{BASE}/{project_id}", json={"status": "active"}, headers=await _admin_headers())
        assert r.status_code == 200
        assert r.json()["status"] == "active"

    async def test_invalid_transition_draft_to_completed_returns_409(self):
        project = await _create_project()
        project_id = project["id"]
        async with httpx.AsyncClient(base_url=BASE_URL, timeout=10) as c:
            r = await c.patch(f"{BASE}/{project_id}", json={"status": "completed"}, headers=await _admin_headers())
        assert r.status_code == 409


@pytest.mark.asyncio
class TestPhases:
    async def test_create_phase_returns_201(self):
        project = await _create_project()
        project_id = project["id"]
        async with httpx.AsyncClient(base_url=BASE_URL, timeout=10) as c:
            r = await c.post(
                f"{BASE}/{project_id}/phases",
                json={"name": "Fase Inicial"},
                headers=await _admin_headers(),
            )
        assert r.status_code == 201
        data = r.json()
        assert data["name"] == "Fase Inicial"
        assert data["status"] == "planned"

    async def test_update_phase_valid_transition(self):
        project = await _create_project()
        project_id = project["id"]
        headers = await _admin_headers()
        async with httpx.AsyncClient(base_url=BASE_URL, timeout=10) as c:
            phase_r = await c.post(
                f"{BASE}/{project_id}/phases",
                json={"name": f"Phase {uuid4().hex[:6]}"},
                headers=headers,
            )
            phase_id = phase_r.json()["id"]
            r = await c.patch(
                f"{BASE}/{project_id}/phases/{phase_id}",
                json={"status": "active"},
                headers=headers,
            )
        assert r.status_code == 200
        assert r.json()["status"] == "active"


@pytest.mark.asyncio
class TestMembers:
    async def test_add_member_returns_201(self):
        project = await _create_project()
        project_id = project["id"]
        user_id = await _get_employee_user_id()
        async with httpx.AsyncClient(base_url=BASE_URL, timeout=10) as c:
            r = await c.post(
                f"{BASE}/{project_id}/members",
                json={"user_id": user_id},
                headers=await _admin_headers(),
            )
        assert r.status_code == 201
        assert str(r.json()["user_id"]) == user_id

    async def test_add_duplicate_member_returns_409(self):
        project = await _create_project()
        project_id = project["id"]
        user_id = await _get_employee_user_id()
        headers = await _admin_headers()
        async with httpx.AsyncClient(base_url=BASE_URL, timeout=10) as c:
            await c.post(f"{BASE}/{project_id}/members", json={"user_id": user_id}, headers=headers)
            r = await c.post(f"{BASE}/{project_id}/members", json={"user_id": user_id}, headers=headers)
        assert r.status_code == 409
