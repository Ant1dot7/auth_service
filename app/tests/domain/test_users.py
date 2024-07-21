import pytest

from domain.entities.users import User
from domain.values.users import UserName, Password, Email
from domain.events.users import NewUserEvent
from domain.exceptions.users import ShortValueException, InvalidEmailException, InvalidPasswordException


class TestUserNameValue:
    def test_create_username(self):
        fake_username = 'username'
        username = UserName(value=fake_username)
        assert username.as_json() == fake_username

    def test_create_short_username(self):
        fake_username = '123'
        with pytest.raises(ShortValueException):
            UserName(value=fake_username)


class TestPasswordValue:
    def test_create_password(self):
        fake_password = 'password'
        password = Password(value=fake_password)
        password.verify_password(fake_password)
        assert password.as_json() != fake_password

    def test_create_short_password(self):
        fake_password = '123'
        with pytest.raises(ShortValueException):
            Password(value=fake_password)

    def test_error_verify_password(self):
        password = Password(value='password')
        with pytest.raises(InvalidPasswordException):
            password.verify_password('password2')


class TestEmailValue:
    def test_create_email(self):
        fake_email = 'email@email.com'
        email = Email(fake_email)
        assert email.as_json() == fake_email

    def test_create_invalid_email(self):
        fake_email = 'email.com'
        with pytest.raises(InvalidEmailException):
            Email(value=fake_email)


def test_create_user():
    password = 'password'
    username = UserName('username')
    password_value = Password(password)
    email = Email('email@email.com')
    user = User.create_user(username=username, password=password_value, email=email)
    user.password.verify_password(password)
    with pytest.raises(InvalidPasswordException):
        user.password.verify_password('password2')
    assert len(user._events) == 1
    assert isinstance(user.pull_events()[0], NewUserEvent)
    assert len(user._events) == 0
