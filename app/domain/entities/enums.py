from enum import Enum


class RoleEnum(str, Enum):
    superuser = "superuser", 4
    admin = "admin", 3
    employee = "employee", 2
    customer = "customer", 1

    def __new__(cls, value, level):
        obj = str.__new__(cls, value)
        obj._value_ = value
        obj.level = level
        return obj

    @property
    def level(self):
        return self._level_

    @level.setter
    def level(self, level):
        self._level_ = level
