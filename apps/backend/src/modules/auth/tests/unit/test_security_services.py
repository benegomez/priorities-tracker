import pytest
from unittest.mock import patch
from datetime import datetime, timedelta, timezone
from uuid import uuid4

from src.shared.security.password_service import PasswordService
from src.shared.security.jwt_service import JwtService, TokenError


class TestPasswordService:
    def test_hash_password_is_not_plaintext(self):
        plain = "MySecret123!"
        hashed = PasswordService.hash_password(plain)
        assert hashed != plain
        assert len(hashed) > 0

    def test_verify_correct_password_returns_true(self):
        plain = "MySecret123!"
        hashed = PasswordService.hash_password(plain)
        assert PasswordService.verify_password(plain, hashed) is True

    def test_verify_wrong_password_returns_false(self):
        hashed = PasswordService.hash_password("CorrectPassword")
        assert PasswordService.verify_password("WrongPassword", hashed) is False


class TestJwtService:
    @patch("src.shared.security.jwt_service.settings")
    def test_create_access_token_contains_required_claims(self, mock_settings):
        mock_settings.JWT_SECRET = "test-secret"
        mock_settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES = 15

        user_id = uuid4()
        org_id = uuid4()
        role = "employee"

        token = JwtService.create_access_token(user_id, org_id, role)
        payload = JwtService.decode_token(token)

        assert payload["sub"] == str(user_id)
        assert payload["organization_id"] == str(org_id)
        assert payload["role"] == role
        assert "exp" in payload
        assert payload["type"] == "access"

    @patch("src.shared.security.jwt_service.settings")
    def test_decode_expired_token_raises_exception(self, mock_settings):
        mock_settings.JWT_SECRET = "test-secret"
        mock_settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES = -1  # already expired

        user_id = uuid4()
        org_id = uuid4()
        token = JwtService.create_access_token(user_id, org_id, "employee")

        with pytest.raises(TokenError):
            JwtService.decode_token(token)

    @patch("src.shared.security.jwt_service.settings")
    def test_decode_invalid_signature_raises_exception(self, mock_settings):
        mock_settings.JWT_SECRET = "correct-secret"
        mock_settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES = 15

        token = JwtService.create_access_token(uuid4(), uuid4(), "employee")

        mock_settings.JWT_SECRET = "wrong-secret"
        with pytest.raises(TokenError):
            JwtService.decode_token(token)
