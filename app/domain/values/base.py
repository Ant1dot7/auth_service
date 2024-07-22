from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any

from domain.exceptions.users import UpdateTypeException


@dataclass(eq=False)
class BaseValue[Value: Any](ABC):
    _need_validate: bool = field(default=True, kw_only=True)
    value: Value

    def __post_init__(self):
        if self._need_validate:
            self.validate()

    def as_json(self) -> Value:
        return self.value

    def update_value(self, new_value: Any):

        if self.value is not None and self.value.__class__ != new_value.__class__:
            raise UpdateTypeException
        self.value = new_value
        self.validate()

    @abstractmethod
    def validate(self):
        ...
