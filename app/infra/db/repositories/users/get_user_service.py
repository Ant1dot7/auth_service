from abc import ABC
from dataclasses import dataclass

from domain.entities.users import User
from infra.common.jwt_service import TokenJwt
from infra.db.repositories.users.base import BaseUserRepository
from infra.exceptions.users import UserHasNoAccessException, UserNotVerifyException


@dataclass(eq=False)
class GetUserByToken(ABC):
    user_repository: BaseUserRepository
    token_service: TokenJwt

    async def get_user(self, token: str, loaded: bool = True) -> User:
        payload = self.token_service.verify_jwt_token(token)
        if loaded:
            return await self.user_repository.get_user(**payload["sub"])
        return await self.user_repository.get_user_not_load(**payload["sub"])

    async def get_verify_user(self, token: str, loaded: bool = True):
        user = await self.get_user(token, loaded)
        if not user.verify:
            raise UserNotVerifyException(user.username.as_json())
        return user

    async def get_admin_user(self, token: str):
        user = await self.get_user(token)
        if not user.is_admin:
            raise UserHasNoAccessException(user.username.as_json())
        return user
