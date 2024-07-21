from abc import ABC
from dataclasses import dataclass, field
from uuid import uuid4


@dataclass(eq=False)
class BaseEvent(ABC):
    event_id: str = field(default_factory=lambda: str(uuid4()), kw_only=True)
