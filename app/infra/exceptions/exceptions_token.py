from dataclasses import dataclass

from infra.exceptions.base import InfraException


@dataclass(eq=False)
class BaseTokenException(InfraException):
    @property
    def message(self) -> str:
        return "Invalid auth token"


@dataclass(eq=False)
class TokenHasExpireException(BaseTokenException):
    @property
    def message(self) -> str:
        return "Token has expired"


@dataclass(eq=False)
class TokenDecodeException(BaseTokenException):
    @property
    def message(self) -> str:
        return "Error decode token"
