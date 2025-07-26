from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.repositories.user_repository import UserRepository
from app.infrastructure.database.session import get_async_db
from app.infrastructure.services.user_service_impl import UserServiceImpl
from app.interfaces.repositories.user_repository_impl import UserRepositoryImpl

async def get_user_repository(
        db: AsyncSession = Depends(get_async_db),
) -> UserRepository:
    return UserRepositoryImpl(db=db)

async def get_user_service(
        user_repository: UserRepository = Depends(get_user_repository),
):
    return UserServiceImpl(user_repository=user_repository)