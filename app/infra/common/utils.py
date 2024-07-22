from dataclasses import dataclass
from datetime import datetime, timedelta, UTC

import jwt

from infra.exceptions.token import TokenHasExpireException, TokenDecodeException


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
