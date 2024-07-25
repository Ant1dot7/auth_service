from email.message import EmailMessage

from common.schemas import MailConf
from jinja2 import Environment, FileSystemLoader
from pyinstrument import Profiler


def profile_timer(func):
    async def wrapper(*args, **kwargs):
        profiler = Profiler(interval=0.0001, async_mode="enabled")
        profiler.start()
        result = await func(*args, **kwargs)
        profiler.stop()
        profiler.print()
        return result

    return wrapper


def build_msg(mail_conf: MailConf) -> EmailMessage:
    env = Environment(loader=FileSystemLoader("/"))
    htm_template = env.get_template(mail_conf.path_template)
    mail = htm_template.render(mail_conf.context)
    email = EmailMessage()
    email["Subject"] = mail_conf.subject
    email["From"] = mail_conf.smtp_user
    email["To"] = mail_conf.to_send_email
    email.set_content(
        mail,
        subtype="html",
    )
    return email
