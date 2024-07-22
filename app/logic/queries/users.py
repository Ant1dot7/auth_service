from dataclasses import dataclass

from domain.entities.users import User as UserEntity
from infra.filters.users import GetUserByTokenFilter
from infra.db.repositories.users.get_user_service import GetUserByToken
from logic.queries.base import BaseQuery
from logic.queries.base import QueryHandler


@dataclass(eq=False)
class GetUserByTokenQuery(BaseQuery):
    filters: GetUserByTokenFilter


@dataclass(eq=False)
class GetVerifyUserQueryHandler(QueryHandler[GetUserByTokenQuery, UserEntity]):
    get_user_service: GetUserByToken

    async def handle(self, query: GetUserByTokenQuery) -> UserEntity:
        user = await self.get_user_service.get_verify_user(token=query.filters.token)
        return user
