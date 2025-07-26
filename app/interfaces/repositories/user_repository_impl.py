from typing import List, Optional
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.domain.mappers.user_mapper import map_user_db_to_user
from app.domain.models.user import User
from app.domain.repositories.user_repository import UserRepository
from app.infrastructure.database.models import UserDB
from app.interfaces.api.schemas.user.edit_user import EditUserRequest
from app.shared.validators.email_validator import validate_email


class UserRepositoryImpl(UserRepository):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_user_by_id(self, user_id: UUID) -> Optional[User]:
        stmt = select(UserDB).where(UserDB.id == user_id)
        result = await self.db.execute(stmt)
        user_db = result.scalar_one_or_none()

        if not user_db:
            raise HTTPException(status_code=404, detail="User not found")

        return map_user_db_to_user(user_db)

    async def get_user_by_email(self, email: str) -> Optional[User]:
        validate_email(email)

        stmt = select(UserDB).where(UserDB.email == email)
        result = await self.db.execute(stmt)
        user_db = result.scalar_one_or_none()

        if not user_db:
            raise HTTPException(status_code=404, detail="User not found")

        return map_user_db_to_user(user_db)

    async def update_user(self, user_id: UUID, user_data: EditUserRequest) -> str:
        stmt = select(UserDB).where(UserDB.id == user_id)
        result = await self.db.execute(stmt)
        user_db = result.scalar_one_or_none()

        if not user_db:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        user_db.email = user_data.email
        user_db.username = user_data.username
        user_db.surname = user_data.surname

        self.db.add(user_db)
        await self.db.commit()
        await self.db.refresh(user_db)

        return "User updated"

    async def delete_user(self, user_id: UUID) -> str:
        stmt = select(UserDB).where(UserDB.id == user_id)
        result = await self.db.delete(stmt)
        print(result)
        return "User deleted"

    async def block_user(self, user_id: UUID) -> str:
        stmt = select(UserDB).where(UserDB.id == user_id)
        result = await self.db.execute(stmt)
        user_db = result.scalar_one_or_none()

        if not user_db:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        user_db.block = True
        await self.db.commit()
        return "User blocked"

    async def unblock_user(self, user_id: UUID) -> str:
        stmt = select(UserDB).where(UserDB.id == user_id)
        result = await self.db.execute(stmt)
        user_db = result.scalar_one_or_none()

        if not user_db:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        user_db.block = False
        await self.db.commit()
        return "User unblocked"

    async def get_users_by_role(self, role: str) -> List[User]:
        pass