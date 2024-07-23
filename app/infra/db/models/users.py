from datetime import date

from sqlalchemy import String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from infra.db.models.base import BaseModel, Base


class UserRole(Base):
    __tablename__ = "user_role"
    id: Mapped[int] = mapped_column(primary_key=True)
    role: Mapped[str] = mapped_column(String(30), unique=True, index=True)

    users = relationship('User', back_populates='role')


class User(BaseModel):
    __tablename__ = "user"

    username: Mapped[str] = mapped_column(String(30), unique=True)
    password: Mapped[str]
    email: Mapped[str]
    verify: Mapped[bool] = mapped_column(Boolean, default=False)
    date_birth: Mapped[date | None]
    first_name: Mapped[str | None] = mapped_column(String(50), nullable=True)
    last_name: Mapped[str | None] = mapped_column(String(50), nullable=True)
    bio: Mapped[str | None]
    avatar: Mapped[str | None]

    role_id: Mapped[int] = mapped_column(ForeignKey('user_role.id'))
    role = relationship('UserRole', back_populates='users')
