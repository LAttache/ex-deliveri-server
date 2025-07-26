from uuid import UUID

from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials
from starlette import status

from app.domain.models.user import User
from app.core.security.tokens import security
from app.domain.services.auth_service import AuthService
from app.infrastructure.dependencies.get_auth_service import get_auth_service


async def get_current_user(
        credentials: HTTPAuthorizationCredentials = Depends(security),
        auth_service: AuthService = Depends(get_auth_service),
) -> User:
    token = credentials.credentials
    try:
        payload = await auth_service.decode_token(token)
        print(payload)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )

    user = await auth_service.get_current_user(UUID(payload["sub"]))
    print(user)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user
