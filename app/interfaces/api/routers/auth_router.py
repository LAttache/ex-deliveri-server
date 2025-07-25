from fastapi import APIRouter, Depends

from app.domain.repositories.auth_repository import AuthRepository
from app.infrastructure.dependencies.auth import get_auth_repository
from app.interfaces.api.schemas.auth.code import CodeRequest, NewCodeRequest
from app.interfaces.api.schemas.auth.login import LoginResponse, LoginRequest
from app.interfaces.api.schemas.auth.registr import RegistrationRequest, RegistrationResponse
from app.use_cases.auth.code import CodeUseCase
from app.use_cases.auth.login import LoginUseCase
from app.use_cases.auth.new_code import NewCodeUseCase
from app.use_cases.auth.register import RegisterUseCase

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login", response_model=LoginResponse)
async def login(
        request: LoginRequest,
        auth_repo: AuthRepository = Depends(get_auth_repository),
):
    use_case = LoginUseCase(auth_repo)
    tokens = await use_case.execute(request)
    return LoginResponse(**tokens.__dict__)


@router.post("/logout")
async def logout():
    pass

@router.post("/register", response_model=RegistrationResponse)
async def register(
        request: RegistrationRequest,
        auth_repo: AuthRepository = Depends(get_auth_repository),
):
    use_case = RegisterUseCase(auth_repo)
    return await use_case.execute(request)

@router.post("/confirm-email")
async def confirm_email(
        request: CodeRequest,
        auth_repo: AuthRepository = Depends(get_auth_repository),
):
    use_case = CodeUseCase(auth_repo)
    tokens = await use_case.execute(request)
    return LoginResponse(**tokens.__dict__)

@router.post("/reset-password")
async def reset_password():
    pass

@router.post("/send-new-code")
async def send_new_code(
        request: NewCodeRequest,
        auth_repo: AuthRepository = Depends(get_auth_repository),
):
    use_case = NewCodeUseCase(auth_repo)
    return await use_case.execute(request)