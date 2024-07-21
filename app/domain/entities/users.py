from dataclasses import dataclass, field
from datetime import date

from domain.entities.base import BaseEntity
from domain.events.users import NewUserEvent
from domain.values.users import UserName, Password, Email


@dataclass(eq=False)
class User(BaseEntity):
    username: UserName
    password: Password
    email: Email
    verify: bool = field(default=False, kw_only=True)
    date_birth: date = field(default=None, kw_only=True)
    avatar: str = field(default=None, kw_only=True)

    @classmethod
    def create_user(cls, **create_data) -> 'User':
        user = cls(**create_data)
        user.register_event(NewUserEvent(email=user.email.as_json()))
        return user
