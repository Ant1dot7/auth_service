from dataclasses import dataclass

from domain.entities.users import User as UserEntity
from domain.values.users import UserName, Password, Email
from infra.db.repositories.users.base import BaseUserRepository
from infra.exceptions.users import UserAlreadyExists
from infra.services.token.jwt import TokenJwt
from logic.commands.base import BaseCommand
from logic.commands.base import CommandHandler


@dataclass(eq=False)
class CreateUserCommand(BaseCommand):
    username: str
    password: str
    email: str
    date_birth: str | None


@dataclass(eq=False)
class CreateUserCommandHandler(CommandHandler[CreateUserCommand, UserEntity]):
    user_repository: BaseUserRepository

    async def handle(self, command: CreateUserCommand) -> UserEntity:
        if await self.user_repository.exists_user(username=command.username):  # Todo рефактор
            raise UserAlreadyExists(command.username)

        user = UserEntity.create_user(
            username=UserName(command.username),
            password=Password(command.password),
            email=Email(command.email),
            date_birth=command.date_birth,
        )
        events = user.pull_events()  # TODO email
        user = await self.user_repository.create_user(user)
        return user


@dataclass(eq=False)
class CreateTokenCommand(BaseCommand):
    username: str
    password: str


@dataclass(eq=False)
class CreateTokenCommandHandler(CommandHandler[CreateTokenCommand, dict]):
    user_repository: BaseUserRepository
    token_service: TokenJwt

    async def handle(self, command: CreateUserCommand) -> str:
        user = await self.user_repository.get_user(username=command.username)
        user.password.verify_password(command.password)
        access_token = self.token_service.create_token(user_id=user.id, expire=10)
        return access_token
