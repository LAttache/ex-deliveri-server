from abc import ABC, abstractmethod

from app.interfaces.api.schemas.auth.code import CodeRequest, NewCodeRequest
from app.interfaces.api.schemas.auth.login import LoginResponse, LoginRequest
from app.interfaces.api.schemas.auth.registr import RegistrationRequest


class AuthRepository(ABC):
    @abstractmethod
    async def login(self, data: LoginRequest) -> LoginResponse:
        pass

    @abstractmethod
    async def logout(self) -> None:
        pass

    @abstractmethod
    async def register(self, data: RegistrationRequest) -> str:
        pass

    @abstractmethod
    async def code_confirmation(self, code: CodeRequest) -> LoginResponse:
        pass

    @abstractmethod
    async def send_new_code(self, data: NewCodeRequest) -> str:
        pass

    @abstractmethod
    async def reset_password(self, email: str) -> str:
        pass