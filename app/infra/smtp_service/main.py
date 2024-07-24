import smtplib
from dataclasses import dataclass
from email.message import EmailMessage

from infra.smtp_service.email_schema import MailConf
from jinja2 import Environment, FileSystemLoader
from settings.config import Settings


@dataclass(eq=False)
class MessageBuilder:
    smtp_user: str

    def build(self, mail_conf: MailConf) -> EmailMessage:
        env = Environment(loader=FileSystemLoader("/"))
        htm_template = env.get_template(mail_conf.path_template)
        mail = htm_template.render(mail_conf.context)
        email = EmailMessage()
        email["Subject"] = mail_conf.subject
        email["From"] = self.smtp_user
        email["To"] = mail_conf.to_send_email
        email.set_content(
            mail,
            subtype="html",
        )
        return email


@dataclass(eq=False)
class SendMail:
    settings: Settings

    def send(self, message: EmailMessage):
        with smtplib.SMTP_SSL(self.settings.smtp_host, self.settings.smtp_port) as server:
            server.login(self.settings.smtp_user, self.settings.smtp_password)
            server.send_message(message)
