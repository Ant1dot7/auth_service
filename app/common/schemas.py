from collections.abc import Mapping
from typing import Any

from pydantic import BaseModel


class MailConf(BaseModel):
    to_send_email: str
    path_template: str
    subject: str
    context: Mapping[str, Any]

    smtp_host: str
    smtp_port: int
    smtp_user: str
    smtp_password: str
