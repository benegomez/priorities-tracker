from datetime import datetime, timedelta, timezone
from uuid import UUID

from jose import JWTError, jwt

from src.shared.config.settings import settings


class TokenError(Exception):
    pass


class JwtService:
    @staticmethod
    def create_access_token(user_id: UUID, organization_id: UUID, role: str) -> str:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
        payload = {
            "sub": str(user_id),
            "organization_id": str(organization_id),
            "role": role,
            "exp": expire,
            "type": "access",
        }
        return jwt.encode(payload, settings.JWT_SECRET, algorithm="HS256")

    @staticmethod
    def create_refresh_token(user_id: UUID) -> str:
        expire = datetime.now(timezone.utc) + timedelta(days=settings.JWT_REFRESH_TOKEN_EXPIRE_DAYS)
        payload = {
            "sub": str(user_id),
            "exp": expire,
            "type": "refresh",
        }
        return jwt.encode(payload, settings.JWT_REFRESH_SECRET, algorithm="HS256")

    @staticmethod
    def decode_token(token: str, *, refresh: bool = False) -> dict:
        secret = settings.JWT_REFRESH_SECRET if refresh else settings.JWT_SECRET
        try:
            return jwt.decode(token, secret, algorithms=["HS256"])
        except JWTError as e:
            raise TokenError(str(e)) from e
