# -*- coding: utf-8 -*-
# website: https://loovien.github.io
# author: luowen<bigpao.luo@gmail.com>
# time: 2018/9/29 21:41
# desc: notify sms or email

import logging
import smtplib
from email.message import EmailMessage

SMTP_PORT = 465
SMTP_URL = "smtp.qq.com"
POP_PORT = 995
POP_URL = "pop.qq.com"

USER = "975753874@qq.com"
PASSWORD_QQ_SMTP = "asexuudrrqxuebeic"
PASSWORD_QQ_POP = "tvcfinugrhjbbejia"

MAIL_TO = "2242430415@qq.com"
MAIL_SENDER = "975753874@qq.com"

logger = logging.getLogger(__name__)


class Reporting(object):
    def __init__(self, receiver: str = None):
        self.receiver = receiver
        self.smtp = smtplib.SMTP_SSL(SMTP_URL, SMTP_PORT)
        self.smtp.login(USER, PASSWORD_QQ_SMTP)

    def sender(self, data: str = None, subject: str = None):
        message = EmailMessage()
        message["subject"] = subject
        message["to"] = self.receiver if self.receiver is not None else MAIL_TO
        message["from"] = MAIL_SENDER
        message["sender"] = MAIL_SENDER
        message.set_content(data)
        self.smtp.send_message(message)

    def dispose(self):
        self.smtp.close()
