from dataclasses import dataclass
from datetime import datetime, timedelta, UTC

import jwt

from domain.entities.users import User
from infra.db.repositories.users.base import BaseUserRepository
from infra.exceptions.token import TokenHasExpireException, TokenDecodeException
from infra.exceptions.users import UserNotVerifyException


@dataclass(eq=False)
class TokenJwt:
    key: str
    algorithm: str

    def create_token(self, sub: dict, expire: int) -> str:
        expires = datetime.now(UTC) + timedelta(minutes=expire)
        payload = {"sub": sub, "exp": expires}
        token = jwt.encode(payload, key=self.key, algorithm=self.algorithm)
        return token

    def verify_jwt_token(self, token: str) -> dict:
        """
        Decodes the token and returns
        its payload as a dictionary.
        """
        try:
            payload = jwt.decode(token, key=self.key, algorithms=self.algorithm)
            return payload
        except jwt.ExpiredSignatureError:
            raise TokenHasExpireException
        except jwt.PyJWTError:
            raise TokenDecodeException


@dataclass(eq=False)
class GetUserByTokenService:
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
