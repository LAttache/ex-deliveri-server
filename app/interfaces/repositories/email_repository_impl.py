from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.repositories.email_repository import EmailRepository
from app.domain.services.email_service import EmailService
from app.infrastructure.database.models import LoginToken


class EmailRepositoryImpl(EmailRepository):
    def __init__(self, db: AsyncSession, email_service: EmailService):
        self.db = db
        self.email_service = email_service

    async def send_email(self, to: str, subject: str, body: str, code: str) -> None:
        await self.db.execute(delete(LoginToken).where(LoginToken.email == to))
        self.db.add(LoginToken(email=to, code=code))
        await self.db.commit()


