from abc import ABC
from dataclasses import dataclass, field
from datetime import datetime
from uuid import uuid4

from domain.events.base import BaseEvent
from domain.values.base import BaseValue


class NotLoaded:
    def __bool__(self) -> bool:
        return False

    def __repr__(self) -> str:
        return "<NotLoaded>"


@dataclass
class BaseEntity(ABC):
    oid: str = field(default_factory=lambda: str(uuid4()), kw_only=True)
    id: int = field(default=None, kw_only=True)
    created_at: datetime = field(default_factory=datetime.now, kw_only=True)
    updated_at: datetime = field(default=None, kw_only=True)
    _events: list[BaseEvent] = field(default_factory=list, kw_only=True)

    def __hash__(self) -> int:
        return hash(self.oid)

    def __eq__(self, other: "BaseEntity") -> bool:
        return self.oid == other.oid

    def register_event(self, event: BaseEvent):
        self._events.append(event)

    def pull_events(self) -> list[BaseEvent]:
        pulled_events = self._events.copy()
        self._events.clear()
        return pulled_events

    def to_update(self, **kwargs):
        for key, value in kwargs.items():
            current_attr = getattr(self, key)
            if isinstance(current_attr, BaseValue):
                current_attr.update_value(value)
            else:
                setattr(self, key, value)
        self.updated_at = datetime.now()
