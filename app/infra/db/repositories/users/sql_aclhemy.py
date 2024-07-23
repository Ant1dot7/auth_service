from dataclasses import dataclass

from domain.entities.users import User as UserEntity, UserRole as UserRoleEntity
from infra.converters.users import (
    convert_user_dto_to_entity,
    convert_user_entity_to_dict,
    convert_user_role_dto_to_entity,
)
from infra.db.models.users import User as UserDto, UserRole as UserRoleDto
from infra.db.repositories.sql_aclhemy_base import SqlAlchemyRepository
from infra.db.repositories.users.base import BaseUserRepository, BaseUserRoleRepository
from infra.exceptions.users import UserDoesNotExists
from sqlalchemy import select
from sqlalchemy.orm import joinedload


class UserRoleRepository(SqlAlchemyRepository[UserRoleDto], BaseUserRoleRepository):
    async def get_role(self, **filters) -> UserRoleEntity:
        role_dto = await self.find_one_or_none(**filters)
        return convert_user_role_dto_to_entity(role_dto)


@dataclass(eq=False)
class UserRepository(SqlAlchemyRepository[UserDto], BaseUserRepository):

    async def create_user(self, user: UserEntity) -> UserEntity:
        user_dto = await self.add_one(**convert_user_entity_to_dict(user))
        return convert_user_dto_to_entity(user_dto)

    async def get_user(self, **filters) -> UserEntity:
        async with self.database.get_read_only_session() as session:
            query = select(self.model).filter_by(**filters).options(joinedload(self.model.role))
            user_dto = (await session.execute(query)).scalar_one_or_none()
            if not user_dto:
                raise UserDoesNotExists(filters)
            return convert_user_dto_to_entity(user_dto)

    async def exists_user(self, **filters) -> bool:
        return bool(await self.find_one_or_none(**filters))

    async def update_user(self, user: UserEntity):
        await self.update_obj(user.id, **convert_user_entity_to_dict(user))
