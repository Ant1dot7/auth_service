from dataclasses import dataclass

from domain.events.base import BaseEvent
from domain.values.users import Email, UserName


@dataclass(eq=False)
class NewUserEvent(BaseEvent):
    email: Email
    username: UserName