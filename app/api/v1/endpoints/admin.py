from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_db, require_role
from app.models.user import User, UserRole
from app.repositories.user import user_repository
from app.schemas.user import UserResponse

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/users", response_model=list[UserResponse])
async def get_all_users(
    current_user: User = Depends(require_role(UserRole.ADMIN)),
    session: AsyncSession = Depends(get_db),
) -> list[UserResponse]:
    users = await user_repository.get_all(session)
    return [UserResponse.model_validate(u) for u in users]
