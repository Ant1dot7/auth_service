from dataclasses import dataclass
from typing import Any

from infra.exceptions.base import InfraException


@dataclass(eq=False)
class UserRoleDoesNotExists(InfraException):
    user_data: Any

    @property
    def message(self) -> str:
        return f"User: {self.user_data} does not found"


@dataclass(eq=False)
class UserDoesNotExists(InfraException):
    user_data: Any

    @property
    def message(self) -> str:
        return f"User: {self.user_data} does not found"


@dataclass(eq=False)
class UserAlreadyExists(InfraException):
    username: str

    @property
    def message(self) -> str:
        return f"User: {self.username} already exists"


@dataclass(eq=False)
class UserHasNoAccessException(InfraException):
    username: str

    @property
    def message(self) -> str:
        return f"User: {self.username} has no access for this action"


@dataclass(eq=False)
class UserNotVerifyException(UserHasNoAccessException):
    username: str

    @property
    def message(self) -> str:
        return f"User: {self.username} not verify"


@dataclass(eq=False)
class UserNotAdminException(UserHasNoAccessException):
    username: str

    @property
    def message(self) -> str:
        return f"User: {self.username} not admin"


@dataclass(eq=False)
class RoleAssignmentException(UserHasNoAccessException):
    username: str

    @property
    def message(self) -> str:
        return f"User: {self.username} cannot assign a role higher than his own"


@dataclass(eq=False)
class SelfRoleAssignmentException(InfraException):
    @property
    def message(self) -> str:
        return "The user cannot change his own role"
