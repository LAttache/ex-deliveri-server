from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.domain.repositories.email_repository import EmailRepository
from app.domain.services.email_service import EmailService
from app.infrastructure.database.session import get_async_db
from app.infrastructure.services.email_service_impl import EmailServiceImpl
from app.interfaces.repositories import EmailRepositoryImpl


async def get_email_service() -> EmailService:
    return EmailServiceImpl(
        smtp_host=settings.smtp_host,
        smtp_port=settings.smtp_port,
        username=settings.smtp_username,
        password=settings.smtp_password
    )

async def get_email_repository(
        db: AsyncSession = Depends(get_async_db),
        auth_service: EmailService = Depends(get_email_service),
) -> EmailRepository:
    return EmailRepositoryImpl(db, auth_service)
