from app.domain.repositories.auth_repository import AuthRepository
from app.interfaces.api.schemas.auth.login import LoginResponse, LoginRequest


class LoginUseCase:
    def __init__(self, auth_repo: AuthRepository):
        self.auth_repo = auth_repo

    async def execute(self, data: LoginRequest) -> LoginResponse:
        return await self.auth_repo.login(data)