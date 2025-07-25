from app.domain.repositories.auth_repository import AuthRepository
from app.interfaces.api.schemas.auth.code import CodeRequest
from app.interfaces.api.schemas.auth.login import LoginResponse


class CodeUseCase:
    def __init__(self, auth_repo: AuthRepository):
        self.auth_repo = auth_repo

    async def execute(self, data: CodeRequest) -> LoginResponse:
        return await self.auth_repo.code_confirmation(data)