from uuid import uuid4, UUID
from datetime import datetime, timezone, timedelta

from sqlalchemy import String, DateTime, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database.session import Base

def utcnow():
    return datetime.now(timezone.utc)

def default_expiry():
    return datetime.now(timezone.utc) + timedelta(minutes=10)

class LoginToken(Base):
    __tablename__ = "login_code"

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    email: Mapped[str] = mapped_column(String, index=True)
    code: Mapped[str] = mapped_column(String)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=default_expiry)

    __table_args__ = (
        UniqueConstraint("email", "code", name="uq_login_code"),
    )

