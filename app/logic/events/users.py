from dataclasses import dataclass

from domain.events.users import NewUserEvent
from infra.db.repositories.users.get_user_service import TokenJwt
from logic.events.base import EventHandler


@dataclass(eq=False)
class SendVerifyMailEventHandler(EventHandler):
    token_service: TokenJwt

    async def handle(self, event: NewUserEvent) -> None:
        token = self.token_service.create_token(
            sub={"username": event.username.as_json()},
            expire=30,
        )
        print(token)  # TODO отправлять на мыло
