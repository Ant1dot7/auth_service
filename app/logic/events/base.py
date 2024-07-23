from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Generic, TypeVar

from domain.events.base import BaseEvent


EventResult = TypeVar("EventResult", bound=Any)
Event = TypeVar("Event", bound=BaseEvent)


@dataclass(eq=False)
class EventHandler(ABC, Generic[Event, EventResult]):
    @abstractmethod
    async def handle(self, event: Event) -> EventResult:
        ...
