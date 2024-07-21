from datetime import date, datetime
from typing import Optional

from sqlalchemy.orm import Mapped, mapped_column

from infra.db.models.base import Base


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime]
    updated_at: Mapped[Optional[datetime]]
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    email: Mapped[str]
    date_birth: Mapped[Optional[date]]
    avatar: Mapped[Optional[str]]
