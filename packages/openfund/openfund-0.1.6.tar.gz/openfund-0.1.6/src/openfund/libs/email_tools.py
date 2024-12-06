#!/usr/bin/env python
import ssl
import os
import sys
import logging

import smtplib

from email.mime.text import MIMEText

from email.header import Header
from email.message import EmailMessage
import time

# app = "email_tools"
# logging.basicConfig(
#     format="%(asctime)s %(name)s:%(levelname)s:%(message)s",
#     datefmt="%Y-%m-%d %H:%M:%S",
#     level=logging.DEBUG,
# )

curPath = os.path.abspath(os.path.dirname(__file__))
sys.path.append(curPath)

from prepare_env import get_mail

# logging.info("---- Read config.ini -----")
(email_address, email_password, email_receiver) = get_mail()
# logging.info(
#     "---- Read config.ini Finish!----{0}||{1}".format(email_address, email_receiver)
# )


def mail(topic, content):
    EMAIL_ADDRESS = email_address
    EMAIL_PASSWORD = email_password
    context = ssl.create_default_context()
    sender = EMAIL_ADDRESS
    receiver = email_receiver.split(",")

    subject = topic
    body = content
    msg = EmailMessage()
    msg["subject"] = subject
    msg["From"] = sender
    msg["To"] = receiver
    msg.set_content(body)

    with smtplib.SMTP_SSL("smtp.qq.com", 465, context=context) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)
        print("---- send_message ----\n{0}".format(msg))


if __name__ == "__main__":
    mail("QRR", "BTCUSDT [2023-12-04 21:44:59 ~ 2023-12-04 21:39:59],QRR=9.4 > 5")
