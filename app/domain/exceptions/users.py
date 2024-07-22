from dataclasses import dataclass

from domain.exceptions.base import BaseDomainException


@dataclass(eq=False)
class ShortValueException(BaseDomainException):
    value: str
    length: int

    @property
    def message(self) -> str:
        return f'The length value:{self.value} must be {self.length} or more characters'


@dataclass(eq=False)
class InvalidEmailException(BaseDomainException):
    email: str

    @property
    def message(self) -> str:
        return f'email validation error. Email: {self.email}'


@dataclass(eq=False)
class InvalidPasswordException(BaseDomainException):

    @property
    def message(self) -> str:
        return 'Invalid password'


@dataclass(eq=False)
class UpdateTypeException(BaseDomainException):
    @property
    def message(self) -> str:
        return f'Error type new value'
