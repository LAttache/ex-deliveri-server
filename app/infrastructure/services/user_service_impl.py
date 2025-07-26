from typing import Optional, List
from uuid import UUID

from fastapi import HTTPException, status

from app.domain.models.user import User
from app.domain.services.user_service import UserService
from app.domain.repositories.user_repository import UserRepository


class UserServiceImpl(UserService):
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def get_user_profile(self, user_id: UUID) -> Optional[User]:
        print(user_id)
        user = await self.user_repository.get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return user

    async def get_user_by_id(self, user_id: UUID) -> Optional[User]:
        user = await self.user_repository.get_user_by_id(user_id)

        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        return user

    async def get_user_by_email(self, email: str) -> Optional[User]:
        user = await self.user_repository.get_user_by_email(email)

        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        return user

    async def update_user(self, user: User) -> str:
        return await self.user_repository.update_user(user)

    async def delete_user(self, user_id: UUID) -> str:
        return await self.user_repository.delete_user(user_id)

    async def block_user(self, user_id: UUID) -> str:
        return await self.user_repository.block_user(user_id)

    async def unblock_user(self, user_id: UUID) -> str:
        return await self.user_repository.unblock_user(user_id)

    async def get_users_by_role(self, role: str) -> List[User]:
        users = await self.user_repository.get_users_by_role(role)

        if not users:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        return users
