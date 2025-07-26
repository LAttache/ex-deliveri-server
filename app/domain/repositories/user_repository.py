from abc import ABC, abstractmethod
from typing import Optional, List
from uuid import UUID

from app.domain.models.user import User


class UserRepository(ABC):
    @abstractmethod
    async def get_user_by_id(self, user_id: UUID) -> Optional[User]:
        pass

    @abstractmethod
    async def get_user_by_email(self, email: str) -> Optional[User]:
        pass

    @abstractmethod
    async def update_user(self, user: User) -> str:
        pass

    @abstractmethod
    async def delete_user(self, user_id: UUID) -> str:
        pass

    @abstractmethod
    async def block_user(self, user_id: UUID) -> str:
        pass

    @abstractmethod
    async def unblock_user(self, user_id: UUID) -> str:
        pass

    @abstractmethod
    async def get_users_by_role(self, role: str) -> List[User]:
        pass
