from uuid import UUID

from pydantic import BaseModel

from app.domain.models.user import User


class UserResponse(BaseModel):
    id: UUID
    name: str
    surname: str
    email: str
    is_email_verified: bool
    is_blocked: bool

    @classmethod
    def from_model(cls, user: User) -> "UserResponse":
        return cls(
            id=user.user_id,
            name=user.username,
            surname=user.surname,
            email=user.email,
            is_email_verified=user.is_email_verified,
            is_blocked=user.is_blocked,
        )
