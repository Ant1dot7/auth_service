from dataclasses import dataclass

from common.utils import profile_timer
from domain.entities.users import User as UserEntity
from infra.db.repositories.users.base import BaseUserRepository
from infra.exceptions.users import UserNotVerifyException
from infra.filters.users import GetUserByTokenFilter
from infra.services.token.jwt import TokenJwt
from logic.queries.base import BaseQuery
from logic.queries.base import QueryHandler


@dataclass(eq=False)
class GetUserByTokenQuery(BaseQuery):
    filters: GetUserByTokenFilter


@dataclass(eq=False)
class GetUserByTokenQueryHandler(QueryHandler[GetUserByTokenQuery, UserEntity]):
    user_repository: BaseUserRepository
    token_service: TokenJwt

    async def handle(self, query: GetUserByTokenQuery) -> UserEntity:
        payload = self.token_service.verify_jwt_token(query.filters.token)
        return await self.user_repository.get_user(id=payload['sub'])


@dataclass(eq=False)
class GetVerifyUserQueryHandler(GetUserByTokenQueryHandler):
    async def handle(self, query: GetUserByTokenQuery) -> UserEntity:
        user = await super().handle(query)
        if not user.verify:
            raise UserNotVerifyException(user.username.as_json())
        return user
