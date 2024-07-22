import pytest

from domain.exceptions.users import ShortValueException, InvalidEmailException, InvalidPasswordException, \
    UpdateTypeException
from domain.values.users import UserName, Password, Email, Name


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


class TestNameValue:
    def test_create_name(self):
        fake_name = 'name'
        name = Name(fake_name)
        assert name.as_json() == fake_name.capitalize()

    def test_create_short_name(self):
        with pytest.raises(ShortValueException):
            Name(value='1')

    def test_update_name(self):
        name = Name('fake_name')
        name.update_value('name')
        assert name.as_json() == 'Name'

        with pytest.raises(ShortValueException):
            name.update_value('a')
        with pytest.raises(UpdateTypeException):
            name.update_value(1)

        name = Name(None)
        assert not name.as_json()
        name.update_value('abc')
        assert name.as_json() == "Abc"

        name = Name(None)
        assert not name.as_json()
        with pytest.raises(UpdateTypeException):
            name.update_value(1)