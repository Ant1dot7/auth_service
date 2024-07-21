from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any


@dataclass(eq=False)
class BaseValue[Value: Any](ABC):
    _need_validate: bool = field(default=True, kw_only=True)
    value: Value

    def __post_init__(self):
        if self._need_validate:
            self.validate()

    def as_json(self) -> Value:
        return self.value

    @abstractmethod
    def validate(self):
        ...
