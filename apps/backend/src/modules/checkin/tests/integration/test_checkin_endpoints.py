from uuid import uuid4

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from src.main import app
from src.shared.config.settings import settings
from src.shared.database.session import get_db_session
from src.shared.security.jwt_service import JwtService


ORG_ID = "11111111-1111-1111-1111-111111111111"
EMPLOYEE_ID = "22222222-2222-2222-2222-222222222222"
PHASE_ID = "44444444-4444-4444-4444-444444444444"


def _auth_headers(user_id: str = EMPLOYEE_ID, org_id: str = ORG_ID, role: str = "employee") -> dict:
    token = JwtService.create_access_token(user_id=user_id, organization_id=org_id, role=role)
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
async def client():
    test_engine = create_async_engine(settings.DATABASE_URL, pool_size=5)
    TestSessionFactory = async_sessionmaker(test_engine, class_=AsyncSession, expire_on_commit=False)

    async def _override_get_db_session():
        async with TestSessionFactory() as session:
            yield session

    app.dependency_overrides[get_db_session] = _override_get_db_session

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

    app.dependency_overrides.clear()
    await test_engine.dispose()


class TestCheckInEndpoints:
    @pytest.mark.asyncio
    async def test_endpoint_post_checkin_returns_401_without_token(self, client):
        response = await client.post("/api/v1/checkins/", json={"week_start": "2025-02-03"})
        assert response.status_code == 401

    @pytest.mark.asyncio
    async def test_endpoint_get_current_returns_401_without_token(self, client):
        response = await client.get("/api/v1/checkins/current")
        assert response.status_code == 401

    @pytest.mark.asyncio
    async def test_endpoint_post_checkin_returns_201(self, client):
        response = await client.post(
            "/api/v1/checkins/",
            json={"week_start": "2025-04-07"},
            headers=_auth_headers(),
        )
        assert response.status_code == 201
        data = response.json()
        assert data["status"] == "draft"
        assert data["employee_id"] == EMPLOYEE_ID
        assert data["organization_id"] == ORG_ID

    @pytest.mark.asyncio
    async def test_endpoint_post_checkin_returns_409_duplicate(self, client):
        headers = _auth_headers()
        resp1 = await client.post("/api/v1/checkins/", json={"week_start": "2025-04-14"}, headers=headers)
        assert resp1.status_code == 201
        resp2 = await client.post("/api/v1/checkins/", json={"week_start": "2025-04-14"}, headers=headers)
        assert resp2.status_code == 409
        assert "BR-001" in resp2.json()["detail"]

    @pytest.mark.asyncio
    async def test_endpoint_submit_returns_409_empty(self, client):
        headers = _auth_headers()
        create_resp = await client.post("/api/v1/checkins/", json={"week_start": "2025-04-21"}, headers=headers)
        checkin_id = create_resp.json()["id"]
        response = await client.post(f"/api/v1/checkins/{checkin_id}/submit", headers=headers)
        assert response.status_code == 409
        assert "at least one priority" in response.json()["detail"]

    @pytest.mark.asyncio
    async def test_endpoint_submit_returns_200(self, client):
        headers = _auth_headers()
        create_resp = await client.post("/api/v1/checkins/", json={"week_start": "2025-04-28"}, headers=headers)
        checkin_id = create_resp.json()["id"]

        await client.post("/api/v1/priorities/", json={
            "checkin_id": checkin_id,
            "phase_id": PHASE_ID,
            "title": "Test priority for submit",
            "priority_level": "high",
        }, headers=headers)

        response = await client.post(f"/api/v1/checkins/{checkin_id}/submit", headers=headers)
        assert response.status_code == 200
        assert response.json()["status"] == "submitted"

    @pytest.mark.asyncio
    async def test_endpoint_post_priority_returns_403_wrong_owner(self, client):
        headers_owner = _auth_headers()
        create_resp = await client.post("/api/v1/checkins/", json={"week_start": "2025-05-05"}, headers=headers_owner)
        checkin_id = create_resp.json()["id"]

        other_employee = str(uuid4())
        headers_other = _auth_headers(user_id=other_employee)
        response = await client.post("/api/v1/priorities/", json={
            "checkin_id": checkin_id,
            "phase_id": PHASE_ID,
            "title": "Intruder priority",
            "priority_level": "low",
        }, headers=headers_other)
        assert response.status_code == 403

    @pytest.mark.asyncio
    async def test_endpoint_post_task_returns_201(self, client):
        headers = _auth_headers()
        create_resp = await client.post("/api/v1/checkins/", json={"week_start": "2025-05-12"}, headers=headers)
        checkin_id = create_resp.json()["id"]

        priority_resp = await client.post("/api/v1/priorities/", json={
            "checkin_id": checkin_id,
            "phase_id": PHASE_ID,
            "title": "Priority with task",
            "priority_level": "medium",
        }, headers=headers)
        priority_id = priority_resp.json()["id"]

        response = await client.post(f"/api/v1/priorities/{priority_id}/tasks", json={
            "title": "My task",
        }, headers=headers)
        assert response.status_code == 201
        assert response.json()["status"] == "pending"
