from dataclasses import dataclass

from common.schemas import MailConf
from domain.events.users import NewUserEvent
from infra.db.repositories.users.get_user_service import TokenJwt
from infra.task_iq.tasks import send_smtp_mail
from logic.events.base import EventHandler
from settings.config import Settings


@dataclass(eq=False)
class SendVerifyMailEventHandler(EventHandler):
    token_service: TokenJwt
    settings: Settings

    async def handle(self, event: NewUserEvent) -> None:
        token = self.token_service.create_token(
            sub={"username": event.username.as_json()},
            expire=30,
        )
        conf = MailConf(
            to_send_email=event.email.as_json(),
            path_template=str(self.settings.verify_template_path),
            subject="Verify account",
            context={
                "username": event.username.as_json(),
                "url": f"{self.settings.domain_url}/users/verify/{token}",
            },
            smtp_host=self.settings.smtp_host,
            smtp_port=self.settings.smtp_port,
            smtp_user=self.settings.smtp_user,
            smtp_password=self.settings.smtp_password,
        )

        await send_smtp_mail.kiq(conf)
        print(token)
