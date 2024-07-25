
import aiosmtplib
from common.schemas import MailConf
from common.utils import build_msg
from infra.task_iq.broker import broker


@broker.task
async def send_smtp_mail(mail_conf: MailConf):
    message = build_msg(mail_conf)
    await aiosmtplib.send(
        message,
        hostname=mail_conf.smtp_host,
        port=mail_conf.smtp_port,
        username=mail_conf.smtp_user,
        password=mail_conf.smtp_password,
        use_tls=True,

    )
