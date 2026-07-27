"""
Integration tests for US-012 Admin User Management endpoints.
Runs against the real running API (docker compose up).
Requires: seed data already loaded.
"""
import pytest
import httpx

BASE_URL = "http://localhost:8000"

_TOKEN_CACHE: dict[str, str] = {}


async def _get_token(email: str, password: str) -> str:
    if email not in _TOKEN_CACHE:
        async with httpx.AsyncClient(base_url=BASE_URL, timeout=10) as c:
            resp = await c.post("/api/v1/auth/login", json={"email": email, "password": password})
            _TOKEN_CACHE[email] = resp.json()["access_token"]
    return _TOKEN_CACHE[email]


async def _admin_headers() -> dict:
    token = await _get_token("admin@org-alpha.com", "Admin1234!")
    return {"Authorization": f"Bearer {token}"}


async def _headers(email: str, password: str) -> dict:
    token = await _get_token(email, password)
    return {"Authorization": f"Bearer {token}"}


class TestListUsers:
    async def test_get_users_returns_only_org_users(self):
        headers = await _admin_headers()
        async with httpx.AsyncClient(base_url=BASE_URL, timeout=10) as c:
            resp = await c.get("/api/v1/users", headers=headers)
        assert resp.status_code == 200
        data = resp.json()
        assert "items" in data
        assert "total" in data
        assert data["page"] == 1

    async def test_get_users_filters_by_role(self):
        headers = await _admin_headers()
        async with httpx.AsyncClient(base_url=BASE_URL, timeout=10) as c:
            resp = await c.get("/api/v1/users?role=employee", headers=headers)
        assert resp.status_code == 200
        for item in resp.json()["items"]:
            assert item["role"] == "employee"

    async def test_get_users_filters_by_status(self):
        headers = await _admin_headers()
        async with httpx.AsyncClient(base_url=BASE_URL, timeout=10) as c:
            resp = await c.get("/api/v1/users?status=active", headers=headers)
        assert resp.status_code == 200
        for item in resp.json()["items"]:
            assert item["status"] == "active"

    async def test_employee_gets_403(self):
        headers = await _headers("employee@org-alpha.com", "Employee1234!")
        async with httpx.AsyncClient(base_url=BASE_URL, timeout=10) as c:
            resp = await c.get("/api/v1/users", headers=headers)
        assert resp.status_code == 403

    async def test_manager_gets_403(self):
        headers = await _headers("manager@org-alpha.com", "Manager1234!")
        async with httpx.AsyncClient(base_url=BASE_URL, timeout=10) as c:
            resp = await c.get("/api/v1/users", headers=headers)
        assert resp.status_code == 403

    async def test_unauthenticated_gets_401(self):
        async with httpx.AsyncClient(base_url=BASE_URL, timeout=10) as c:
            resp = await c.get("/api/v1/users")
        assert resp.status_code == 401


class TestCreateUser:
    async def test_post_user_creates_and_returns_201(self):
        import time
        unique_email = f"test_{int(time.time())}@org-alpha.com"
        headers = await _admin_headers()
        async with httpx.AsyncClient(base_url=BASE_URL, timeout=10) as c:
            resp = await c.post(
                "/api/v1/users",
                json={"email": unique_email, "first_name": "Test", "last_name": "User", "role": "employee"},
                headers=headers,
            )
        assert resp.status_code == 201
        data = resp.json()
        assert data["email"] == unique_email
        assert data["status"] == "active"
        assert "temporary_password" in data
        assert len(data["temporary_password"]) >= 12

    async def test_post_user_returns_409_on_duplicate_email(self):
        headers = await _admin_headers()
        async with httpx.AsyncClient(base_url=BASE_URL, timeout=10) as c:
            resp = await c.post(
                "/api/v1/users",
                json={"email": "employee@org-alpha.com", "first_name": "Dup", "last_name": "User", "role": "employee"},
                headers=headers,
            )
        assert resp.status_code == 409


class TestUpdateUser:
    async def test_patch_user_updates_fields(self):
        headers = await _admin_headers()
        async with httpx.AsyncClient(base_url=BASE_URL, timeout=10) as c:
            list_resp = await c.get("/api/v1/users?role=employee", headers=headers)
            users = list_resp.json()["items"]
            if not users:
                pytest.skip("No employees found")
            user_id = users[0]["id"]
            resp = await c.patch(
                f"/api/v1/users/{user_id}",
                json={"first_name": "Updated"},
                headers=headers,
            )
        assert resp.status_code == 200
        assert resp.json()["first_name"] == "Updated"

    async def test_patch_status_deactivates_user(self):
        import time
        unique_email = f"deact_{int(time.time())}@org-alpha.com"
        headers = await _admin_headers()
        async with httpx.AsyncClient(base_url=BASE_URL, timeout=10) as c:
            create_resp = await c.post(
                "/api/v1/users",
                json={"email": unique_email, "first_name": "Deact", "last_name": "User", "role": "employee"},
                headers=headers,
            )
            user_id = create_resp.json()["id"]
            resp = await c.patch(
                f"/api/v1/users/{user_id}/status",
                json={"status": "inactive"},
                headers=headers,
            )
        assert resp.status_code == 200
        assert resp.json()["status"] == "inactive"

    async def test_patch_status_409_on_self_deactivation(self):
        headers = await _admin_headers()
        async with httpx.AsyncClient(base_url=BASE_URL, timeout=10) as c:
            me_resp = await c.get("/api/v1/auth/me", headers=headers)
            admin_id = me_resp.json()["id"]
            resp = await c.patch(
                f"/api/v1/users/{admin_id}/status",
                json={"status": "inactive"},
                headers=headers,
            )
        assert resp.status_code == 409
