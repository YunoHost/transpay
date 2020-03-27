import smtplib
import pystache
import html.parser
from email.mime.text import MIMEText
from email.utils import localtime, format_datetime
from flask import render_template
from flask_babel import gettext

from core.objects import DonationType
from core.config import _cfg, _cfgi
from core.currency import currency


def send_thank_you(user, amount, monthly):
    if _cfg("smtp-host") == "":
        return
    smtp = smtplib.SMTP(_cfg("smtp-host"), _cfgi("smtp-port"))
    smtp.ehlo()
    smtp.starttls()
    smtp.login(_cfg("smtp-user"), _cfg("smtp-password"))
    message = MIMEText(
        render_template(
            "emails/thank-you",
            user=user,
            root=_cfg("protocol") + "://" + _cfg("domain"),
            your_name=_cfg("your-name"),
            amount=currency.amount("{:.2f}".format(amount / 100)),
            monthly=monthly,
            your_email=_cfg("your-email"),
        )
    )
    message["Subject"] = gettext("Thank you for your donation!")
    message["From"] = _cfg("smtp-from")
    message["To"] = user.email
    message["Date"] = format_datetime(localtime())
    smtp.sendmail(_cfg("smtp-from"), [user.email], message.as_string())
    smtp.quit()


def send_password_reset(user):
    if _cfg("smtp-host") == "":
        return
    smtp = smtplib.SMTP(_cfg("smtp-host"), _cfgi("smtp-port"))
    smtp.ehlo()
    smtp.starttls()
    smtp.login(_cfg("smtp-user"), _cfg("smtp-password"))
    message = MIMEText(
        render_template(
            "emails/reset-password",
            user=user,
            root=_cfg("protocol") + "://" + _cfg("domain"),
            your_name=_cfg("your-name"),
            your_email=_cfg("your-email"),
        )
    )
    message["Subject"] = gettext("Reset your donor password")
    message["From"] = _cfg("smtp-from")
    message["To"] = user.email
    message["Date"] = format_datetime(localtime())
    smtp.sendmail(_cfg("smtp-from"), [user.email], message.as_string())
    smtp.quit()


def send_declined(user, amount):
    if _cfg("smtp-host") == "":
        return
    smtp = smtplib.SMTP(_cfg("smtp-host"), _cfgi("smtp-port"))
    smtp.ehlo()
    smtp.starttls()
    smtp.login(_cfg("smtp-user"), _cfg("smtp-password"))
    message = MIMEText(
        render_template(
            "emails/declined",
            user=user,
            root=_cfg("protocol") + "://" + _cfg("domain"),
            your_name=_cfg("your-name"),
            amount=currency.amount("{:.2f}".format(amount / 100)),
        )
    )
    message["Subject"] = gettext("Your monthly donation was declined.")
    message["From"] = _cfg("smtp-from")
    message["To"] = user.email
    message["Date"] = format_datetime(localtime())
    smtp.sendmail(_cfg("smtp-from"), [user.email], message.as_string())
    smtp.quit()


def send_new_donation(user, donation):
    if _cfg("smtp-host") == "":
        return
    smtp = smtplib.SMTP(_cfg("smtp-host"), _cfgi("smtp-port"))
    smtp.ehlo()
    smtp.starttls()
    smtp.login(_cfg("smtp-user"), _cfg("smtp-password"))
    with open("emails/new_donation") as f:
        message = MIMEText(
            html.parser.HTMLParser().unescape(
                pystache.render(
                    f.read(),
                    {
                        "user": user,
                        "root": _cfg("protocol") + "://" + _cfg("domain"),
                        "your_name": _cfg("your-name"),
                        "amount": currency.amount(
                            "{:.2f}".format(donation.amount / 100)
                        ),
                        "frequency": (
                            " per month"
                            if donation.type == DonationType.monthly
                            else ""
                        ),
                        "comment": donation.comment or "",
                    },
                )
            )
        )
    message["Subject"] = "New donation on fosspay!"
    message["From"] = _cfg("smtp-from")
    message["To"] = f"{_cfg('your-name')} <{_cfg('your-email')}>"
    message["Date"] = format_datetime(localtime())
    smtp.sendmail(_cfg("smtp-from"), [_cfg("your-email")], message.as_string())
    smtp.quit()


def send_cancellation_notice(user, donation):
    if _cfg("smtp-host") == "":
        return
    smtp = smtplib.SMTP(_cfg("smtp-host"), _cfgi("smtp-port"))
    smtp.ehlo()
    smtp.starttls()
    smtp.login(_cfg("smtp-user"), _cfg("smtp-password"))
    with open("emails/cancelled") as f:
        message = MIMEText(
            html.parser.HTMLParser().unescape(
                pystache.render(
                    f.read(),
                    {
                        "user": user,
                        "root": _cfg("protocol") + "://" + _cfg("domain"),
                        "your_name": _cfg("your-name"),
                        "amount": currency.amount(
                            "{:.2f}".format(donation.amount / 100)
                        ),
                    },
                )
            )
        )
    message["Subject"] = "A monthly donation on fosspay has been cancelled"
    message["From"] = _cfg("smtp-from")
    message["To"] = f"{_cfg('your-name')} <{_cfg('your-email')}>"
    message["Date"] = format_datetime(localtime())
    smtp.sendmail(_cfg("smtp-from"), [_cfg("your-email")], message.as_string())
    smtp.quit()
