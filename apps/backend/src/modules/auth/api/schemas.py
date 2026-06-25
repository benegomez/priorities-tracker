from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr


class LoginRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", json_schema_extra={
        "example": {"email": "ana@empresa.com", "password": "secreto"}
    })

    email: EmailStr
    password: str


class LoginResponse(BaseModel):
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "access_token": "eyJ...",
            "refresh_token": "eyJ...",
            "token_type": "bearer",
            "expires_in": 900,
        }
    })

    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int


class RefreshRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    refresh_token: str


class RefreshResponse(BaseModel):
    access_token: str
    expires_in: int


class LogoutResponse(BaseModel):
    message: str


class MeResponse(BaseModel):
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "id": "550e8400-e29b-41d4-a716-446655440000",
            "email": "ana@empresa.com",
            "role": "employee",
            "organization_id": "550e8400-e29b-41d4-a716-446655440001",
            "full_name": "Ana López",
        }
    })

    id: UUID
    email: str
    role: str
    organization_id: UUID
    full_name: str
