from fastapi import APIRouter, Depends
from starlette import status
from starlette.responses import Response

from app.domain.models.user import User
from app.domain.services.user_service import UserService
from app.infrastructure.dependencies.get_current_user import get_current_user
from app.infrastructure.dependencies.user import get_user_service
from app.interfaces.api.schemas.user.edit_user import EditUserRequest
from app.interfaces.api.schemas.user.user_response import UserResponse, UpdateUserResponse
from app.use_cases.user.edit_user_info import EditUserInfoUseCase
from app.use_cases.user.get_user_info import GetUserInfoUseCase

router = APIRouter(prefix="/user", tags=["user"])

@router.get("/me", response_model=UserResponse)
async def get_me(
        current_user: User = Depends(get_current_user),
        user_service: UserService = Depends(get_user_service)
):
    use_case = GetUserInfoUseCase(user_service)
    user_info = await use_case.execute(current_user.user_id)

    return UserResponse.from_model(user_info)


@router.put("/me", response_model=UpdateUserResponse)
async def update_current_user(
        request: EditUserRequest,
        current_user: User = Depends(get_current_user),
        user_service: UserService = Depends(get_user_service)
):
    use_case = EditUserInfoUseCase(user_service)
    user_info = await use_case.execute(current_user.user_id, request)

    return Response(status_code=status.HTTP_200_OK, content=user_info)