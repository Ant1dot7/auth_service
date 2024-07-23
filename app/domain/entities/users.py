from dataclasses import dataclass, field
from datetime import date

from domain.entities.base import BaseEntity
from domain.entities.enums import RoleEnum
from domain.events.users import NewUserEvent
from domain.values.users import UserName, Password, Email, Name


@dataclass(eq=False)
class UserRole:
    id: int | None = field(default=None, kw_only=True)
    role: str


@dataclass(eq=False)
class User(BaseEntity):
    username: UserName
    password: Password
    email: Email
    verify: bool = field(default=False, kw_only=True)
    date_birth: date = field(default=None, kw_only=True)
    first_name: Name = field(default=Name(None), kw_only=True)
    last_name: Name = field(default=Name(None), kw_only=True)
    bio: str = field(default=None, kw_only=True)
    avatar: str = field(default=None, kw_only=True)

    role: UserRole = field(default=UserRole(RoleEnum.customer), kw_only=True)

    @classmethod
    def create_user(cls, **create_data) -> 'User':
        user = cls(**create_data)
        user.register_event(NewUserEvent(email=user.email, username=user.username))
        return user
