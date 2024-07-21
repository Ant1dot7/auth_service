from dataclasses import dataclass

from domain.events.base import BaseEvent


@dataclass(eq=False)
class NewUserEvent(BaseEvent):
    email: str