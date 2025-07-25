from app.domain.repositories.auth_repository import AuthRepository
from app.interfaces.api.schemas.auth.code import NewCodeRequest


class NewCodeUseCase:
    def __init__(self, auth_repo: AuthRepository):
        self.auth_repo = auth_repo

    async def execute(self, data: NewCodeRequest) -> str:
        return await self.auth_repo.send_new_code(data)