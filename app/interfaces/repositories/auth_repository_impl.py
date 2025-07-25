from datetime import datetime, timezone
import random

from sqlalchemy import select, delete, and_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from app.domain.models.auth import TokenPair, RegistrationMessage
from app.domain.repositories.auth_repository import AuthRepository
from app.domain.services.auth_service import AuthService
from app.domain.services.email_service import EmailService

from app.interfaces.api.schemas.auth.code import CodeRequest, NewCodeRequest
from app.interfaces.api.schemas.auth.login import LoginRequest
from app.interfaces.api.schemas.auth.registr import RegistrationRequest

from app.infrastructure.database.models import UserDB, LoginToken
from app.shared.validators.email_validator import validate_email


class AuthRepositoryImpl(AuthRepository):
    def __init__(
            self,
            db: AsyncSession,
            auth_service: AuthService,
            email_service: EmailService,
    ):
        self.db = db
        self.auth_service = auth_service
        self.email_service = email_service

    async def login(self, data: LoginRequest) -> TokenPair:
        validate_email(data.email)

        stmt = select(UserDB).where(UserDB.email == data.email)
        result = await self.db.execute(stmt)
        user = result.scalar_one_or_none()

        if not user or not user.verify_password(data.password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

        if not user.is_email_verified:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Email not verified")

        if user.is_blocked:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="User is blocked")

        tokens = await self.auth_service.create_token_pair(user.id)
        return tokens

    async def logout(self) -> None:
        # TODO: реализовать blacklist или invalidate refresh_token
        pass

    async def register(self, data: RegistrationRequest) -> RegistrationMessage:
        validate_email(data.email)

        if len(data.username) == 0:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Username is required"
            )

        user = UserDB(email=data.email, username=data.username)
        user.set_password(data.password)
        self.db.add(user)

        try:
            await self.db.commit()
        except IntegrityError as e:
            await self.db.rollback()

            if 'users_email_key' in str(e.orig):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="User with this email already exists"
                )
            raise

        code = f"{random.randint(1000, 9999)}"

        await self.email_service.send_email(
            to=data.email,
            subject="Ваш код подтверждения регистрации",
            body=f"Здравствуйте!\n\nВаш код подтверждения: {code}\n\nСпасибо за регистрацию!"
        )

        print(code)
        token = LoginToken(email=data.email, code=code)

        try:
            self.db.add(token)
            await self.db.commit()
            print("✅ Token saved successfully!")
        except IntegrityError as e:
            await self.db.rollback()
            print(f"❌ DB error: {e}")

        return RegistrationMessage("Code sent successfully")

    async def code_confirmation(self, data: CodeRequest) -> TokenPair:
        validate_email(data.email)

        stmt = select(LoginToken).where(and_(
            LoginToken.email == data.email,
            LoginToken.code == data.code,
            LoginToken.expires_at >= datetime.now(timezone.utc)
        ))

        result = await self.db.execute(stmt)
        login_code = result.scalar_one_or_none()

        if data.code != login_code.code:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid code")

        user_stmt = select(UserDB).where(UserDB.email == data.email)
        user_result = await self.db.execute(user_stmt)
        user = user_result.scalar_one_or_none()

        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid credentials")

        user.is_email_verified = True
        await self.db.commit()
        return await self.auth_service.create_token_pair(user.id)

    async def send_new_code(self, data: NewCodeRequest) -> str:
        await self._delete_expired_codes()

        code = f"{random.randint(1000, 9999)}"
        print(code)

        await self.db.execute(delete(LoginToken).where(LoginToken.email == data.email))

        try:
            token = LoginToken(email=data.email, code=code)
            self.db.add(token)
            await self.db.commit()
        except IntegrityError as e:
            await self.db.rollback()

        await self.email_service.send_email(
            to=data.email,
            subject="Ваш код подтверждения регистрации",
            body=f"Здравствуйте!\n\nВаш код подтверждения: {code}\n\nСпасибо за регистрацию!"
        )

        return "New token sent to email"

    async def reset_password(self, email: str) -> str:
        return "Password reset link sent"

    async def _delete_expired_codes(self):
        await self.db.execute(
            delete(LoginToken).where(datetime.now(timezone.utc) > LoginToken.expires_at)
        )
        await self.db.commit()
