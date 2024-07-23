from dataclasses import dataclass


@dataclass
class BaseAppException(Exception):
    @property
    def message(self) -> str:
        return "Unknown app error"

    def __str__(self):
        return self.message
