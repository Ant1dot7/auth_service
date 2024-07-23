from dataclasses import dataclass

from domain.exceptions.users import (
    InvalidEmailException,
    InvalidPasswordException,
    ShortValueException,
    UpdateTypeException,
)
from domain.values.base import BaseValue
from email_validator import validate_email
from passlib.hash import bcrypt


@dataclass(eq=False, slots=True)
class UserName(BaseValue[str]):
    value: str

    def validate(self):
        if len(self.value) < 4:
            raise ShortValueException(value=self.value, length=4)


@dataclass(eq=False)
class Password(BaseValue[str]):
    value: str
    need_hash: bool = True

    def __post_init__(self):
        super().__post_init__()
        if self.need_hash:
            self._hash_password()

    def validate(self):
        if len(self.value) < 4:
            raise ShortValueException(value=self.value, length=4)

    def _hash_password(self) -> None:
        self.value = bcrypt.hash(self.value)

    def verify_password(self, password):
        if not bcrypt.verify(password, self.value):
            raise InvalidPasswordException


@dataclass(eq=False)
class Email(BaseValue[str]):
    value: str

    def validate(self):
        try:
            validate_email(self.value)
        except Exception: # noqa
            raise InvalidEmailException(email=self.value)


@dataclass(eq=False)
class Name(BaseValue[str | None]):
    value: str | None

    def __post_init__(self):
        if self.value is not None:
            super().__post_init__()
            self.value = self.value.capitalize()

    def validate(self):
        if len(self.value) < 2:
            raise ShortValueException(value=self.value, length=2)

    def update_value(self, new_value):
        if not isinstance(new_value, str | type(None)):
            raise UpdateTypeException()
        super().update_value(new_value)
        self.value = new_value.capitalize()
