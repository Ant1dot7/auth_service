from datetime import datetime
from typing import Optional

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, declarative_mixin


@declarative_mixin
class BaseMixin:
    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime]
    updated_at: Mapped[Optional[datetime]]


class Base(BaseMixin, DeclarativeBase):
    __abstract__ = True
