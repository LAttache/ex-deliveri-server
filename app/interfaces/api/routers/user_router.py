from fastapi import APIRouter, Depends

from app.domain.models.user import User
from app.infrastructure.dependencies.user import get_current_user

router = APIRouter(prefix="/user", tags=["user"])

@router.get("/me")
async def get_current_user(
        current_user: User = Depends(get_current_user)
):
    pass

@router.put("/me")
async def update_current_user(
        current_user: User = Depends(get_current_user)
):
    pass