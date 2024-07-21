from functools import lru_cache

from punq import Container, Scope

from infra.db.db_config import Database
from infra.db.repositories.users.base import BaseUserRepository
from infra.db.repositories.users.sql_aclhemy import UserRepository
from infra.db.models.users import User
from logic.commands.users import CreateUserCommandHandler, CreateUserCommand, CreateTokenCommandHandler, \
    CreateTokenCommand
from logic.mediator.main_mediator import Mediator
from logic.queries.users import GetUserQuery, GetUserQueryHandler
from settings.config import Settings, get_settings


@lru_cache(1)
def init_container() -> Container:
    return _init_container()


def _init_container() -> Container:
    container = Container()
    container.register(Settings, factory=get_settings, scope=Scope.singleton)

    settings = container.resolve(Settings)
    container.register(
        Database,
        instance=Database(url=settings.db_url, ro_url=settings.db_url),
        scope=Scope.singleton
    )

    container.register(BaseUserRepository, instance=UserRepository(
        model=User,
        database=container.resolve(Database)
    ))

    def init_mediator() -> Mediator:
        mediator = Mediator()

        # COMMAND HANDLERS
        create_user_command_handler = CreateUserCommandHandler(
            user_repository=container.resolve(BaseUserRepository)
        )
        create_token_command_handler = CreateTokenCommandHandler(
            user_repository=container.resolve(BaseUserRepository)
        )

        # QUERY HANDLERS
        get_user_query_handler = GetUserQueryHandler(
            user_repository=container.resolve(BaseUserRepository)
        )

        # REGISTER COMMANDS
        mediator.register_command(CreateUserCommand, [create_user_command_handler])
        mediator.register_command(CreateTokenCommand, [create_token_command_handler])
        # REGISTER QUERY
        mediator.register_query(GetUserQuery, get_user_query_handler)

        return mediator

    container.register(Mediator, factory=init_mediator, scope=Scope.singleton)
    return container
