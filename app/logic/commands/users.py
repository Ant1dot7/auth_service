from dataclasses import dataclass

from domain.entities.enums import RoleEnum
from domain.entities.users import User as UserEntity
from domain.values.users import (
    Email,
    Name,
    Password,
    UserName,
)
from infra.db.repositories.users.base import BaseUserRepository, BaseUserRoleRepository
from infra.db.repositories.users.get_user_service import GetUserByToken, TokenJwt
from infra.exceptions.users import UserAlreadyExists
from infra.s3.client import S3Client
from logic.commands.base import BaseCommand, CommandHandler
from logic.mediator.main_mediator import Mediator
from settings.config import Settings


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
class CreateUserCommandHandler(CommandHandler[CreateUserCommand, int]):
    user_repository: BaseUserRepository
    role_repository: BaseUserRoleRepository
    _mediator: Mediator

    async def handle(self, command: CreateUserCommand) -> int:
        if await self.user_repository.exists_user(username=command.username):  # Todo рефактор
            raise UserAlreadyExists(command.username)
        role = await self.role_repository.get_role(role=RoleEnum.customer.value)
        user = UserEntity.create_user(
            username=UserName(command.username),
            password=Password(command.password),
            email=Email(command.email),
            date_birth=command.date_birth,
            first_name=Name(command.first_name),
            last_name=Name(command.last_name),
            bio=command.bio,
            role=role,
        )
        events = user.pull_events()  # TODO email
        user_id = await self.user_repository.create_user(user)
        await self._mediator.handle_events(events)
        return user_id


@dataclass(eq=False)
class CreateTokenCommand(BaseCommand):
    username: str
    password: str


@dataclass(eq=False)
class CreateTokenCommandHandler(CommandHandler[CreateTokenCommand, str]):
    user_repository: BaseUserRepository
    token_service: TokenJwt

    async def handle(self, command: CreateUserCommand) -> tuple[str, str]:
        user = await self.user_repository.get_user_not_load(username=command.username)
        user.password.verify_password(command.password)

        access_token = self.token_service.create_token(sub={"id": user.id}, expire=15)
        refresh_token = self.token_service.create_token(sub={"id": user.id}, expire=3600)

        return access_token, refresh_token


@dataclass(eq=False)
class VerifyUserCommand(BaseCommand):
    token: str


@dataclass(eq=False)
class VerifyUserCommandHandler(CommandHandler[VerifyUserCommand, None]):
    user_repository: BaseUserRepository
    get_user_service: GetUserByToken

    async def handle(self, command: VerifyUserCommand) -> None:
        user = await self.get_user_service.get_user(command.token, loaded=False)
        user.to_update(verify=True)
        await self.user_repository.update_user(user)


@dataclass(eq=False)
class UpdateUserAvatarCommand(BaseCommand):
    token: str
    avatar: bytes


@dataclass(eq=False)
class UpdateUserAvatarCommandHandler(CommandHandler[UpdateUserAvatarCommand, None]):
    user_repository: BaseUserRepository
    get_user_service: GetUserByToken
    s3_client: S3Client
    settings: Settings

    async def handle(self, command: UpdateUserAvatarCommand) -> None:
        user = await self.get_user_service.get_verify_user(command.token, loaded=False)
        s3_path = f"{user.id}/avatar.png"
        await self.s3_client.upload_file_bytes(
            bucket_name=self.settings.user_bucket,
            file_bytes=command.avatar,
            s3_path=s3_path,
        )
        user.to_update(avatar=f"{self.settings.user_bucket}/{s3_path}")
        await self.user_repository.update_user(user)


@dataclass(eq=False)
class UpdateUserDataCommand(BaseCommand):
    token: str
    data: dict


@dataclass(eq=False)
class UpdateUserDataCommandHandler(CommandHandler[UpdateUserDataCommand, None]):
    user_repository: BaseUserRepository
    get_user_service: GetUserByToken

    async def handle(self, command: UpdateUserDataCommand) -> None:
        user = await self.get_user_service.get_verify_user(command.token, loaded=False)
        user.to_update(**command.data)
        await self.user_repository.update_user(user)
