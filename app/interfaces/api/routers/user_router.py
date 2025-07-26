from fastapi import APIRouter, Depends

from app.domain.models.user import User
from app.domain.services.user_service import UserService
from app.infrastructure.dependencies.get_current_user import get_current_user
from app.infrastructure.dependencies.user import get_user_service
from app.interfaces.api.schemas.user.user_response import UserResponse
from app.use_cases.user.get_user_info import GetUserInfoUseCase

router = APIRouter(prefix="/user", tags=["user"])

@router.get("/me", response_model=UserResponse)
async def get_current_user(
        current_user: User = Depends(get_current_user),
        user_service: UserService = Depends(get_user_service)
):
    use_case = GetUserInfoUseCase(user_service)
    user_info = await use_case.execute(current_user.user_id)
    return UserResponse.from_model(user_info)


@router.put("/me")
async def update_current_user(
        current_user: User = Depends(get_current_user)
):
    pass