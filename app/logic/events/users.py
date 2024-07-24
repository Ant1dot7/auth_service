from dataclasses import dataclass

from domain.events.users import NewUserEvent
from infra.db.repositories.users.get_user_service import TokenJwt
from infra.smtp_service.email_schema import MailConf
from infra.smtp_service.main import MessageBuilder, SendMail
from logic.events.base import EventHandler
from settings.config import Settings


@dataclass(eq=False)
class SendVerifyMailEventHandler(EventHandler):
    token_service: TokenJwt
    send_mail_service: SendMail
    message_builder: MessageBuilder
    settings: Settings

    async def handle(self, event: NewUserEvent) -> None:
        token = self.token_service.create_token(
            sub={"username": event.username.as_json()},
            expire=30,
        )
        message = self.message_builder.build(
            MailConf(
                to_send_email=event.email.as_json(),
                path_template=str(self.settings.verify_template_path),
                subject="Verify account",
                context={
                    "username": event.username.as_json(),
                    "url": f"{self.settings.domain_url}/users/verify/{token}",
                },
            ),
        )
        self.send_mail_service.send(message)  # TODO отправлять через taskiq
        print(token)
