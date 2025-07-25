from app.domain.repositories.auth_repository import AuthRepository
from app.interfaces.api.schemas.auth.registr import RegistrationRequest

class RegisterUseCase:
    def __init__(self, auth_repo: AuthRepository):
        self.auth_repo = auth_repo

    async def execute(self, data: RegistrationRequest) -> str:
        return await self.auth_repo.register(data)