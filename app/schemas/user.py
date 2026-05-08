import uuid
from datetime import datetime

from pydantic import BaseModel, EmailStr

from app.models.user import UserRole


class UserCreate(BaseModel):
    email: EmailStr
    full_name: str
    password: str


class UserResponse(BaseModel):
    id: uuid.UUID
    email: EmailStr
    full_name: str
    is_active: bool
    is_verified: bool
    role: UserRole
    created_at: datetime

    model_config = {"from_attributes": True}
