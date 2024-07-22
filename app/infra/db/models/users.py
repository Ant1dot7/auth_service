from datetime import date

from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from infra.db.models.base import BaseModel


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
