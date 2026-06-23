from typing import Annotated
from uuid import UUID

from fastapi import Depends, Header, HTTPException, status

from src.shared.security.jwt_service import JwtService, TokenError


class CurrentUser:
    def __init__(self, user_id: UUID, organization_id: UUID, role: str) -> None:
        self.user_id = user_id
        self.organization_id = organization_id
        self.role = role


async def get_current_user(
    authorization: Annotated[str | None, Header()] = None,
) -> CurrentUser:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )

    token = authorization.removeprefix("Bearer ")
    try:
        payload = JwtService.decode_token(token)
    except TokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )

    return CurrentUser(
        user_id=UUID(payload["sub"]),
        organization_id=UUID(payload["organization_id"]),
        role=payload["role"],
    )


def require_roles(*roles: str):
    async def _check(current_user: CurrentUser = Depends(get_current_user)) -> CurrentUser:
        if current_user.role not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions",
            )
        return current_user
    return _check
