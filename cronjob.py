#!/usr/bin/env python3
from core.objects import *
from core.database import db
from core.config import _cfg
from core.emails import send_thank_you, send_declined
from core.currency import currency
from core.app import app
from flask_babel import Babel, _, ngettext

from datetime import datetime, timedelta
from babel.dates import format_date, format_datetime, format_time

import requests
import stripe
import subprocess

with app.app_context():
    
    stripe.api_key = _cfg("stripe-secret")

    date = format_date(datetime.now(), locale=_cfg("locale"))
    time = format_time(datetime.now(), locale=_cfg("locale"))
    print(_("Processing monthly donations on"), date, time)
    
    donations = Donation.query \
        .filter(Donation.type == DonationType.monthly) \
        .filter(Donation.active) \
        .all()
    
    limit = datetime.now() - timedelta(days=30)
    
    for donation in donations:
        if donation.updated < limit:
            print(_("Charging {}").format(donation))
            user = donation.user
            customer = stripe.Customer.retrieve(user.stripe_customer)
            try:
                charge = stripe.Charge.create(
                    amount=donation.amount,
                    currency=_cfg("currency"),
                    customer=user.stripe_customer,
                    description=_("Donation to ") + _cfg("your-name")
                )
            except stripe.error.CardError as e:
                donation.active = False
                db.commit()
                send_declined(user, donation.amount)
                print(_("Declined"))
                continue
    
            send_thank_you(user, donation.amount, donation.type == DonationType.monthly)
            donation.updated = datetime.now()
            donation.payments += 1
            db.commit()
        else:
            print(_("Skipping {}").format(donation))
    
    print(ngettext(u'%(num)d record processed.\n', u'%(num)d records processed.\n', num=len(donations)))
    
    if _cfg("patreon-refresh-token"):
        print(_("Updating Patreon API token"))
    
        r = requests.post('https://www.patreon.com/api/oauth2/token', params={
            'grant_type': 'refresh_token',
            'refresh_token': _cfg("patreon-refresh-token"),
            'client_id': _cfg("patreon-client-id"),
            'client_secret': _cfg("patreon-client-secret")
        })
        if r.status_code != 200:
            print(_("Failed to update Patreon API token"))
            sys.exit(1)
        resp = r.json()
        with open("config.ini") as f:
            config = f.read()
        config = config.replace(_cfg("patreon-access-token"), resp["access_token"])
        config = config.replace(_cfg("patreon-refresh-token"), resp["refresh_token"])
        with open("config.ini", "w") as f:
            f.write(config)
        print(_("Refreshed Patreon API token"))
        reload_cmd = _cfg("reload-command")
        if not reload_cmd:
            print(_("Cannot reload application, add reload-command to config.ini"))
        else:
            subprocess.run(reload_cmd, shell=True, check=True)
