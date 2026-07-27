from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    role: str
    manager_id: UUID | None = None


class UserUpdate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    role: str | None = None
    manager_id: UUID | None = None
    new_password: str | None = None


class UserStatusUpdate(BaseModel):
    status: str


class UserResponse(BaseModel):
    id: UUID
    email: str
    first_name: str
    last_name: str
    role: str
    status: str
    manager_id: UUID | None
    manager_name: str | None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    model_config = {"from_attributes": True}


class UserCreatedResponse(UserResponse):
    temporary_password: str


class UserListResponse(BaseModel):
    items: list[UserResponse]
    total: int
    page: int
    page_size: int
    pages: int


class UserStatusResponse(BaseModel):
    id: UUID
    status: str
