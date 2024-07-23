from dataclasses import dataclass

from common.exceptions import BaseAppException


@dataclass(eq=False)
class BaseDomainException(BaseAppException):
    @property
    def message(self) -> str:
        return "Unknown domain error"
