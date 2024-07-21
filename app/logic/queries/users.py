from dataclasses import dataclass

from common.utils import profile_timer
from domain.entities.users import User as UserEntity
from infra.db.repositories.users.base import BaseUserRepository
from infra.filters.users import GetUserByIdFilter
from logic.queries.base import BaseQuery
from logic.queries.base import QueryHandler


@dataclass(eq=False)
class GetUserQuery(BaseQuery):
    filters: GetUserByIdFilter


@dataclass(eq=False)
class GetUserQueryHandler(QueryHandler[GetUserQuery, UserEntity]):
    user_repository: BaseUserRepository

    async def handle(self, query: GetUserQuery) -> UserEntity:
        return await self.user_repository.get_user(id=query.filters.user_id)
