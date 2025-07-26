from uuid import UUID

from app.domain.models.user import User
from app.domain.services.user_service import UserService


class GetUserInfoUseCase:
    def __init__(self, user_service: UserService):
        self.user_service = user_service

    async def execute(self, user_id: UUID) -> User:
        return await self.user_service.get_user_by_id(user_id)
