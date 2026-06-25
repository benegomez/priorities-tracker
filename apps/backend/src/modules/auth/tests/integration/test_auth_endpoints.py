"""
Integration tests for auth endpoints.
These tests run against the real running API (docker compose up).
Requires: seed data already loaded.
"""
import pytest
import httpx

BASE_URL = "http://localhost:8000"


@pytest.fixture
def client():
    return httpx.AsyncClient(base_url=BASE_URL, timeout=10)


class TestLoginEndpoint:
    async def test_endpoint_login_returns_200_with_valid_credentials(self, client):
        async with client:
            response = await client.post("/api/v1/auth/login", json={
                "email": "admin@org-alpha.com",
                "password": "Admin1234!",
            })
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data
        assert data["token_type"] == "bearer"
        assert data["expires_in"] == 900

    async def test_endpoint_login_returns_401_with_wrong_password(self, client):
        async with client:
            response = await client.post("/api/v1/auth/login", json={
                "email": "admin@org-alpha.com",
                "password": "WrongPassword",
            })
        assert response.status_code == 401
        assert response.json()["detail"] == "Invalid credentials"

    async def test_endpoint_login_returns_403_for_inactive_user(self, client):
        async with client:
            response = await client.post("/api/v1/auth/login", json={
                "email": "inactive@org-alpha.com",
                "password": "Inactive1234!",
            })
        assert response.status_code == 403

    async def test_login_error_message_does_not_reveal_which_field_failed(self, client):
        async with client:
            response = await client.post("/api/v1/auth/login", json={
                "email": "nonexistent@example.com",
                "password": "anything",
            })
        assert response.status_code == 401
        detail = response.json()["detail"]
        assert "email" not in detail.lower()
        assert "password" not in detail.lower()


class TestRefreshEndpoint:
    async def test_endpoint_refresh_returns_200_with_valid_token(self, client):
        async with client:
            login_resp = await client.post("/api/v1/auth/login", json={
                "email": "employee@org-alpha.com",
                "password": "Employee1234!",
            })
            rt = login_resp.json()["refresh_token"]

            response = await client.post("/api/v1/auth/refresh", json={
                "refresh_token": rt,
            })
        assert response.status_code == 200
        assert "access_token" in response.json()
        assert response.json()["expires_in"] == 900

    async def test_endpoint_refresh_returns_401_with_invalid_token(self, client):
        async with client:
            response = await client.post("/api/v1/auth/refresh", json={
                "refresh_token": "invalid.token.here",
            })
        assert response.status_code == 401


class TestLogoutEndpoint:
    async def test_endpoint_logout_returns_200_and_revokes_token(self, client):
        async with client:
            login_resp = await client.post("/api/v1/auth/login", json={
                "email": "manager@org-alpha.com",
                "password": "Manager1234!",
            })
            tokens = login_resp.json()
            at = tokens["access_token"]
            rt = tokens["refresh_token"]

            response = await client.post(
                "/api/v1/auth/logout",
                json={"refresh_token": rt},
                headers={"Authorization": f"Bearer {at}"},
            )
            assert response.status_code == 200
            assert response.json()["message"] == "logged out"

            # Verify token is revoked
            refresh_resp = await client.post("/api/v1/auth/refresh", json={"refresh_token": rt})
            assert refresh_resp.status_code == 401


class TestMeEndpoint:
    async def test_endpoint_me_returns_user_info_with_valid_token(self, client):
        async with client:
            login_resp = await client.post("/api/v1/auth/login", json={
                "email": "admin@org-alpha.com",
                "password": "Admin1234!",
            })
            at = login_resp.json()["access_token"]

            response = await client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {at}"})
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == "admin@org-alpha.com"
        assert data["role"] == "administrator"
        assert data["full_name"] == "Admin Alpha"
        assert "organization_id" in data

    async def test_endpoint_me_returns_401_without_token(self, client):
        async with client:
            response = await client.get("/api/v1/auth/me")
        assert response.status_code == 401


class TestSecurity:
    async def test_jwt_secret_not_present_in_response_body(self, client):
        async with client:
            response = await client.post("/api/v1/auth/login", json={
                "email": "admin@org-alpha.com",
                "password": "Admin1234!",
            })
        body_str = response.text
        assert "changeme" not in body_str.lower()
