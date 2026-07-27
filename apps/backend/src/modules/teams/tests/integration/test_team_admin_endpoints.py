"""Integration tests for admin team management endpoints."""
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


async def _admin_headers() -> dict:
    return {"Authorization": f"Bearer {await _get_token('admin@org-alpha.com', 'Admin1234!')}"}


async def _employee_headers() -> dict:
    return {"Authorization": f"Bearer {await _get_token('employee@org-alpha.com', 'Employee1234!')}"}


async def _manager_headers() -> dict:
    return {"Authorization": f"Bearer {await _get_token('manager@org-alpha.com', 'Manager1234!')}"}


@pytest.mark.asyncio
class TestListTeams:
    async def test_returns_paginated_list(self):
        async with httpx.AsyncClient(base_url=BASE_URL, timeout=10) as c:
            r = await c.get(BASE, headers=await _admin_headers())
        assert r.status_code == 200
        data = r.json()
        assert "items" in data
        assert "total" in data

    async def test_employee_gets_403(self):
        async with httpx.AsyncClient(base_url=BASE_URL, timeout=10) as c:
            r = await c.get(BASE, headers=await _employee_headers())
        assert r.status_code == 403

    async def test_manager_gets_403(self):
        async with httpx.AsyncClient(base_url=BASE_URL, timeout=10) as c:
            r = await c.get(BASE, headers=await _manager_headers())
        assert r.status_code == 403


@pytest.mark.asyncio
class TestCreateTeam:
    async def test_creates_team_returns_201(self):
        name = f"New Team {uuid4().hex[:6]}"
        async with httpx.AsyncClient(base_url=BASE_URL, timeout=10) as c:
            r = await c.post(BASE, json={"name": name}, headers=await _admin_headers())
        assert r.status_code == 201
        data = r.json()
        assert data["name"] == name
        assert "id" in data
        assert data["member_count"] == 0

    async def test_returns_409_on_duplicate_name(self):
        name = f"Dup Team {uuid4().hex[:6]}"
        headers = await _admin_headers()
        async with httpx.AsyncClient(base_url=BASE_URL, timeout=10) as c:
            await c.post(BASE, json={"name": name}, headers=headers)
            r = await c.post(BASE, json={"name": name}, headers=headers)
        assert r.status_code == 409


@pytest.mark.asyncio
class TestGetTeamDetail:
    async def test_returns_detail_with_members(self):
        name = f"Detail Team {uuid4().hex[:6]}"
        headers = await _admin_headers()
        async with httpx.AsyncClient(base_url=BASE_URL, timeout=10) as c:
            create_r = await c.post(BASE, json={"name": name}, headers=headers)
            team_id = create_r.json()["id"]
            r = await c.get(f"{BASE}/{team_id}", headers=headers)
        assert r.status_code == 200
        data = r.json()
        assert data["id"] == team_id
        assert "members" in data

    async def test_returns_404_for_unknown_team(self):
        async with httpx.AsyncClient(base_url=BASE_URL, timeout=10) as c:
            r = await c.get(f"{BASE}/{uuid4()}", headers=await _admin_headers())
        assert r.status_code == 404


@pytest.mark.asyncio
class TestUpdateTeam:
    async def test_updates_name(self):
        name = f"Update Team {uuid4().hex[:6]}"
        new_name = f"Updated {uuid4().hex[:6]}"
        headers = await _admin_headers()
        async with httpx.AsyncClient(base_url=BASE_URL, timeout=10) as c:
            create_r = await c.post(BASE, json={"name": name}, headers=headers)
            team_id = create_r.json()["id"]
            r = await c.patch(f"{BASE}/{team_id}", json={"name": new_name}, headers=headers)
        assert r.status_code == 200
        assert r.json()["name"] == new_name


@pytest.mark.asyncio
class TestTeamMembers:
    async def test_add_and_remove_member(self):
        headers = await _admin_headers()
        async with httpx.AsyncClient(base_url=BASE_URL, timeout=10) as c:
            # create team
            team_r = await c.post(BASE, json={"name": f"Members Team {uuid4().hex[:6]}"}, headers=headers)
            team_id = team_r.json()["id"]

            # get an employee
            users_r = await c.get("/api/v1/users?role=employee", headers=headers)
            users = users_r.json()["items"]
            if not users:
                pytest.skip("No employee users available")
            user_id = users[0]["id"]

            # add member
            add_r = await c.post(f"{BASE}/{team_id}/members", json={"user_id": user_id}, headers=headers)
            assert add_r.status_code == 200
            assert add_r.json()["user_id"] == user_id

            # verify in detail
            detail_r = await c.get(f"{BASE}/{team_id}", headers=headers)
            assert user_id in [m["id"] for m in detail_r.json()["members"]]

            # remove member
            del_r = await c.delete(f"{BASE}/{team_id}/members/{user_id}", headers=headers)
            assert del_r.status_code == 204

    async def test_add_member_409_when_already_member(self):
        headers = await _admin_headers()
        async with httpx.AsyncClient(base_url=BASE_URL, timeout=10) as c:
            team_r = await c.post(BASE, json={"name": f"Dup Member {uuid4().hex[:6]}"}, headers=headers)
            team_id = team_r.json()["id"]

            users_r = await c.get("/api/v1/users?role=employee", headers=headers)
            users = users_r.json()["items"]
            if not users:
                pytest.skip("No employee users available")
            user_id = users[0]["id"]

            await c.post(f"{BASE}/{team_id}/members", json={"user_id": user_id}, headers=headers)
            r = await c.post(f"{BASE}/{team_id}/members", json={"user_id": user_id}, headers=headers)
            assert r.status_code == 409

            # cleanup
            await c.delete(f"{BASE}/{team_id}/members/{user_id}", headers=headers)
