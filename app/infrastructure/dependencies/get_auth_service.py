from fastapi import Depends

from app.domain.repositories.user_repository import UserRepository
from app.domain.services.auth_service import AuthService
from app.infrastructure.dependencies.user import get_user_repository
from app.infrastructure.services.auth_service_impl import JWTAuthService


async def get_auth_service(
        user_repository: UserRepository = Depends(get_user_repository),
) -> AuthService:
    return JWTAuthService(user_repository=user_repository)
