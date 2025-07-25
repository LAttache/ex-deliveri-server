from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.services.email_service import EmailService
from app.infrastructure.database.session import get_async_db
from app.infrastructure.dependencies.email import get_email_service
from app.infrastructure.services.auth_service_impl import JWTAuthService
from app.domain.services.auth_service import AuthService
from app.domain.repositories.auth_repository import AuthRepository
from app.interfaces.repositories.auth_repository_impl import AuthRepositoryImpl


async def get_auth_service() -> AuthService:
    return JWTAuthService()

async def get_auth_repository(
        db: AsyncSession = Depends(get_async_db),
        auth_service: AuthService = Depends(get_auth_service),
        email_service: EmailService = Depends(get_email_service)
) -> AuthRepository:
    return AuthRepositoryImpl(db, auth_service, email_service)
