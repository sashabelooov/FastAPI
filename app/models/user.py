import enum

from sqlalchemy import Boolean, Enum as SAEnum, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import TimeStampedBase


class UserRole(str, enum.Enum):
    USER = "user"
    ADMIN = "admin"


class User(TimeStampedBase):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    full_name: Mapped[str] = mapped_column(String, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    role: Mapped[UserRole] = mapped_column(
        SAEnum(UserRole), default=UserRole.USER, nullable=False
    )
    todos: Mapped[list["Todo"]] = relationship("Todo", back_populates="owner")
