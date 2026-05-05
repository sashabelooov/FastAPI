from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.user import user_repository
from app.schemas.user import UserCreate, UserResponse
from app.core.security import verify_password, create_access_token, create_refresh_token


class AuthService:
    async def register(self, session: AsyncSession, data: UserCreate) -> UserResponse:
        existing = await user_repository.get_by_email(session, data.email)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )
        user = await user_repository.create(session, data)
        return UserResponse.model_validate(user)

    async def login(self, session: AsyncSession, email: str, password: str) -> dict:
        user = await user_repository.get_by_email(session, email)
        if not user or not verify_password(password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
            )
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Account is disabled",
            )
        return {
            "access_token": create_access_token(user.email),
            "refresh_token": create_refresh_token(user.email),
            "token_type": "bearer",
        }


auth_service = AuthService()