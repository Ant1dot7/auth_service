from dataclasses import dataclass

from domain.entities.users import User as UserEntity
from infra.converters.users import convert_user_entity_to_dict, convert_user_dto_to_entity
from infra.exceptions.users import UserDoesNotExists
from infra.db.repositories.sql_aclhemy_base import SqlAlchemyRepository
from infra.db.repositories.users.base import BaseUserRepository
from infra.db.models.users import User as UserDto


@dataclass(eq=False)
class UserRepository(SqlAlchemyRepository[UserDto], BaseUserRepository):
    async def create_user(self, user: UserEntity) -> UserEntity:
        user_dto = await self.add_one(**convert_user_entity_to_dict(user))
        return convert_user_dto_to_entity(user_dto)

    async def get_user(self, **filters) -> UserEntity:
        user_dto = await self.find_one_or_none(**filters)
        print(user_dto)
        if not user_dto:
            raise UserDoesNotExists(filters)
        return convert_user_dto_to_entity(user_dto)

    async def exists_user(self, **filters) -> bool:
        return bool(await self.find_one_or_none(**filters))
