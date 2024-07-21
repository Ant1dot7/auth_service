from dataclasses import dataclass
from typing import Any

from infra.exceptions.base import InfraException


@dataclass(eq=False)
class UserDoesNotExists(InfraException):
    user_data: Any

    @property
    def message(self) -> str:
        return f'User: {self.user_data} does not found'


@dataclass(eq=False)
class UserAlreadyExists(InfraException):
    username: str

    @property
    def message(self) -> str:
        return f'User: {self.username} already exists'
