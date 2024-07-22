from abc import ABC
from dataclasses import dataclass

from domain.entities.users import User
from infra.common.utils import TokenJwt
from infra.db.repositories.users.base import BaseUserRepository
from infra.exceptions.users import UserNotVerifyException


@dataclass(eq=False)
class GetUserByToken(ABC):
    user_repository: BaseUserRepository
    token_service: TokenJwt

    async def get_user(self, token: str) -> User:
        payload = self.token_service.verify_jwt_token(token)
        return await self.user_repository.get_user(**payload['sub'])

    async def get_verify_user(self, token: str):
        user = await self.get_user(token)
        if not user.verify:
            raise UserNotVerifyException(user.username.as_json())
        return user
