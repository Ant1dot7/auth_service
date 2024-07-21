from dataclasses import dataclass

from common.exceptions import BaseAppException


@dataclass(eq=False)
class InfraException(BaseAppException):
    @property
    def message(self) -> str:
        return 'Infra Error'
