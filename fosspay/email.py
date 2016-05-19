import smtplib
import pystache
import os
import html.parser
from email.mime.text import MIMEText
from werkzeug.utils import secure_filename
from flask import url_for

from fosspay.database import db
from fosspay.objects import User
from fosspay.config import _cfg, _cfgi

def send_thank_you(user, amount, monthly):
    if _cfg("smtp-host") == "":
        return
    smtp = smtplib.SMTP(_cfg("smtp-host"), _cfgi("smtp-port"))
    smtp.ehlo()
    smtp.starttls()
    smtp.login(_cfg("smtp-user"), _cfg("smtp-password"))
    with open("emails/thank-you") as f:
        message = MIMEText(html.parser.HTMLParser().unescape(\
            pystache.render(f.read(), {
                "user": user,
                "root": _cfg("protocol") + "://" + _cfg("domain"),
                "your_name": _cfg("your-name"),
                "amount": "{:.2f}".format(amount / 100),
                "monthly": monthly,
                "your_email": _cfg("your-email")
            })))
    message['Subject'] = "Thank you for your donation!"
    message['From'] = _cfg("smtp-from")
    message['To'] = user.email
    smtp.sendmail(_cfg("smtp-from"), [ user.email ], message.as_string())
    smtp.quit()

def send_password_reset(user):
    if _cfg("smtp-host") == "":
        return
    smtp = smtplib.SMTP(_cfg("smtp-host"), _cfgi("smtp-port"))
    smtp.ehlo()
    smtp.starttls()
    smtp.login(_cfg("smtp-user"), _cfg("smtp-password"))
    with open("emails/reset-password") as f:
        message = MIMEText(html.parser.HTMLParser().unescape(\
            pystache.render(f.read(), {
                "user": user,
                "root": _cfg("protocol") + "://" + _cfg("domain"),
                "your_name": _cfg("your-name"),
                "your_email": _cfg("your-email")
            })))
    message['Subject'] = "Reset your donor password"
    message['From'] = _cfg("smtp-from")
    message['To'] = user.email
    smtp.sendmail(_cfg("smtp-from"), [ user.email ], message.as_string())
    smtp.quit()

def send_declined(user, amount):
    if _cfg("smtp-host") == "":
        return
    smtp = smtplib.SMTP(_cfg("smtp-host"), _cfgi("smtp-port"))
    smtp.ehlo()
    smtp.starttls()
    smtp.login(_cfg("smtp-user"), _cfg("smtp-password"))
    with open("emails/declined") as f:
        message = MIMEText(html.parser.HTMLParser().unescape(\
            pystache.render(f.read(), {
                "user": user,
                "root": _cfg("protocol") + "://" + _cfg("domain"),
                "your_name": _cfg("your-name"),
                "amount": "{:.2f}".format(amount / 100)
            })))
    message['Subject'] = "Your monthly donation was declined."
    message['From'] = _cfg("smtp-from")
    message['To'] = user.email
    smtp.sendmail(_cfg("smtp-from"), [ user.email ], message.as_string())
    smtp.quit()
