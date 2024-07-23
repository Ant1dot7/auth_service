import pytest

from domain.entities.users import User
from domain.events.users import NewUserEvent
from domain.exceptions.users import InvalidPasswordException
from domain.values.users import (
    Email,
    Name,
    Password,
    UserName,
)


def test_create_user():
    password = "password"
    user = User.create_user(
        username=UserName("username"),
        password=Password(password),
        email=Email("email@email.com"),
    )
    user.password.verify_password(password)
    with pytest.raises(InvalidPasswordException):
        user.password.verify_password("password2")
    assert user.first_name.as_json() is None
    assert user.last_name.as_json() is None
    assert len(user._events) == 1
    assert isinstance(user.pull_events()[0], NewUserEvent)
    assert len(user._events) == 0


def test_create_user_with_first_last_name():
    password = "password"
    user = User.create_user(
        username=UserName("username"),
        password=Password(password),
        email=Email("email@email.com"),
        first_name=Name("first_name"),
        last_name=Name("last_name"),
    )
    user.password.verify_password(password)
    with pytest.raises(InvalidPasswordException):
        user.password.verify_password("password2")
    assert user.first_name.as_json() == "First_name"
    assert user.last_name.as_json() == "Last_name"
    assert len(user._events) == 1
    assert isinstance(user.pull_events()[0], NewUserEvent)
    assert len(user._events) == 0
