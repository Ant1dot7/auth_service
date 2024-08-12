from dataclasses import dataclass

from logic.commands.base import BaseCommand


@dataclass(eq=False)
class CreateUserCommand(BaseCommand):
    username: str
    password: str
    email: str
    date_birth: str | None
    first_name: str | None
    last_name: str | None
    bio: str | None


@dataclass(eq=False)
class CreateTokenCommand(BaseCommand):
    username: str
    password: str


@dataclass(eq=False)
class VerifyUserCommand(BaseCommand):
    token: str


@dataclass(eq=False)
class UpdateUserAvatarCommand(BaseCommand):
    token: str
    avatar: bytes


@dataclass(eq=False)
class UpdateUserDataCommand(BaseCommand):
    token: str
    data: dict


@dataclass(eq=False)
class UpdateUserRoleCommand(BaseCommand):
    token: str
    user_id: int
    role_id: int
