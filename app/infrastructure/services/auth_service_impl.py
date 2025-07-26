from uuid import UUID
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException, status

from app.core.config import settings
from app.domain.models.auth import TokenPair
from app.domain.models.user import User
from app.domain.repositories.user_repository import UserRepository
from app.domain.services.auth_service import AuthService

class JWTAuthService(AuthService):
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def get_current_user(self, param) -> User:
        user = await self.user_repository.get_user_by_id(param)

        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        return user

    async def create_token_pair(self, user_id: UUID) -> TokenPair:
        return  TokenPair(
            await self._create_token(user_id, settings.access_token_expiration, "access"),
            await self._create_token(user_id, settings.refresh_token_expiration, "refresh")
        )

    @staticmethod
    async def _create_token(user_id: UUID, expires_delta: timedelta, token_type: str) -> str:
        now = datetime.now(timezone.utc)
        expire = now + expires_delta
        to_encode = {
            "sub": str(user_id),
            "exp": expire,
            "iat": now,
            "nbf": now,
            "type": token_type
        }
        return jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)

    async def decode_token(self, token: str) -> dict:
        try:
            return jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        except JWTError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    async def verify_access_token(self, token: str) -> UUID:
        payload = await self.decode_token(token)
        if payload.get("type") != "access":
            raise HTTPException(status_code=401, detail="Wrong token type")
        try:
            return UUID(payload["sub"])
        except ValueError:
            raise HTTPException(status_code=401, detail="Invalid user ID")
