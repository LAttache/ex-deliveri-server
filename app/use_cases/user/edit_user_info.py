from uuid import UUID

from app.domain.services.user_service import UserService
from app.interfaces.api.schemas.user.edit_user import EditUserRequest


class EditUserInfoUseCase:
    def __init__(
            self,
            user_service: UserService
    ):
        self.user_service = user_service

    async def execute(self, user_id: UUID, user: EditUserRequest) -> str:
        return await self.user_service.update_user(user_id=user_id, user=user)