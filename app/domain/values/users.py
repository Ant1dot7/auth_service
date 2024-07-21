from dataclasses import dataclass

from passlib.hash import bcrypt

from domain.exceptions.users import ShortValueException, InvalidPasswordException, InvalidEmailException
from domain.values.base import BaseValue
from email_validator import validate_email


@dataclass(eq=False)
class UserName(BaseValue[str]):
    value: str

    def validate(self):
        if len(self.value) < 4:
            raise ShortValueException(value=self.value, length=4)


@dataclass(eq=False)
class Password(BaseValue):
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
class Email(BaseValue):
    value: str

    def validate(self):
        try:
            validate_email(self.value)
        except Exception:
            raise InvalidEmailException(email=self.value)
