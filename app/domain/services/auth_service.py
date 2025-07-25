from abc import ABC, abstractmethod
from uuid import UUID

from app.domain.models.auth import TokenPair
from app.domain.models.user import User


class AuthService(ABC):
    @abstractmethod
    async def create_token_pair(self, user_id: UUID) -> TokenPair:
        pass

    @abstractmethod
    async def decode_token(self, token: str) -> dict:
        pass

    @abstractmethod
    async def verify_access_token(self, token: str) -> UUID:
        pass

    async def get_current_user(self, param) -> User:
        pass
