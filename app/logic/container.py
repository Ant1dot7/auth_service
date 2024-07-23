from functools import lru_cache

from punq import Container, Scope

from domain.events.users import NewUserEvent
from infra.common.utils import TokenJwt
from infra.db.db_config import Database
from infra.db.repositories.users.base import BaseUserRepository, BaseUserRoleRepository
from infra.db.repositories.users.sql_aclhemy import UserRepository, UserRoleRepository
from infra.db.models.users import User, UserRole
from infra.db.repositories.users.get_user_service import GetUserByToken
from infra.s3.client import S3Client
from logic.commands.users import CreateUserCommandHandler, CreateUserCommand, CreateTokenCommandHandler, \
    CreateTokenCommand, VerifyUserCommandHandler, VerifyUserCommand, UpdateUserAvatarCommandHandler, \
    UpdateUserAvatarCommand, UpdateUserDataCommandHandler, UpdateUserDataCommand
from logic.events.users import SendVerifyMailEventHandler
from logic.mediator.main_mediator import Mediator
from logic.queries.users import GetUserByTokenQuery, GetVerifyUserQueryHandler
from settings.config import Settings, get_settings


@lru_cache(1)
def init_container() -> Container:
    return _init_container()


def _init_container() -> Container:
    container = Container()
    container.register(Settings, factory=get_settings, scope=Scope.singleton)

    settings: Settings = container.resolve(Settings)
    # DB register
    container.register(
        Database,
        instance=Database(url=settings.db_url, ro_url=settings.db_url),
        scope=Scope.singleton
    )

    container.register(BaseUserRepository, instance=UserRepository(
        model=User,
        database=container.resolve(Database)
    ))
    container.register(BaseUserRoleRepository, instance=UserRoleRepository(
        model=UserRole,
        database=container.resolve(Database)
    ))

    container.register(
        TokenJwt,
        instance=TokenJwt(settings.jwt_key, settings.jwt_alg),
        scope=Scope.singleton
    )

    container.register(
        GetUserByToken,
        instance=GetUserByToken(
            user_repository=container.resolve(BaseUserRepository),
            token_service=container.resolve(TokenJwt),
        )
    )
    container.register(
        S3Client,
        instance=S3Client(
            aws_access_key_id=settings.aws_access_key_id,
            aws_secret_access_key=settings.aws_secret_access_key,
            endpoint_url=settings.s3_url,
        ),
        scope=Scope.singleton,
    )

    def init_mediator() -> Mediator:
        mediator = Mediator()

        # COMMAND HANDLERS
        create_user_command_handler = CreateUserCommandHandler(
            user_repository=container.resolve(BaseUserRepository),
            role_repository=container.resolve(BaseUserRoleRepository),
            _mediator=mediator
        )
        create_token_command_handler = CreateTokenCommandHandler(
            user_repository=container.resolve(BaseUserRepository),
            token_service=container.resolve(TokenJwt),
        )
        verify_user_command_handler = VerifyUserCommandHandler(
            user_repository=container.resolve(BaseUserRepository),
            get_user_service=container.resolve(GetUserByToken),
        )
        update_user_avatar_command_handler = UpdateUserAvatarCommandHandler(
            user_repository=container.resolve(BaseUserRepository),
            get_user_service=container.resolve(GetUserByToken),
            s3_client=container.resolve(S3Client),
            settings=settings,
        )
        update_user_data_command_handler = UpdateUserDataCommandHandler(
            user_repository=container.resolve(BaseUserRepository),
            get_user_service=container.resolve(GetUserByToken),
        )

        # EVENT HANDLERS
        send_verify_token = SendVerifyMailEventHandler(token_service=container.resolve(TokenJwt))

        # QUERY HANDLERS
        get_user_by_token_query_handler = GetVerifyUserQueryHandler(
            get_user_service=container.resolve(GetUserByToken),
        )

        # REGISTER COMMANDS
        mediator.register_command(CreateUserCommand, [create_user_command_handler])
        mediator.register_command(CreateTokenCommand, [create_token_command_handler])
        mediator.register_command(VerifyUserCommand, [verify_user_command_handler])
        mediator.register_command(UpdateUserAvatarCommand, [update_user_avatar_command_handler])
        mediator.register_command(UpdateUserDataCommand, [update_user_data_command_handler])

        # REGISTER QUERY
        mediator.register_query(GetUserByTokenQuery, get_user_by_token_query_handler)

        # REGISTER EVENT
        mediator.register_event(NewUserEvent, [send_verify_token])
        return mediator

    container.register(Mediator, factory=init_mediator, scope=Scope.singleton)
    return container
