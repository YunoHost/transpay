#!/usr/bin/env python3
from fosspay.objects import *
from fosspay.database import db
from fosspay.config import _cfg
from fosspay.email import send_thank_you, send_declined

from datetime import datetime, timedelta

import stripe

stripe.api_key = _cfg("stripe-secret")

print("Processing monthly donations")

donations = Donation.query \
    .filter(Donation.type == DonationType.monthly) \
    .filter(Donation.active) \
    .all()

limit = datetime.now() - timedelta(days=30)

for donation in donations:
    if donation.updated < limit:
        print("Charging {}".format(donation))
        user = donation.user
        customer = stripe.Customer.retrieve(user.stripe_customer)
        try:
            charge = stripe.Charge.create(
                amount=donation.amount,
                currency="usd",
                customer=user.stripe_customer,
                description="Donation to " + _cfg("your-name")
            )
        except stripe.error.CardError as e:
            donation.active = False
            db.commit()
            send_declined(user, donation.amount)
            print("Declined")
            continue

        send_thank_you(user, donation.amount, donation.type == DonationType.monthly)
        donation.updated = datetime.now()
        donation.payments += 1
        db.commit()
    else:
        print("Skipping {}".format(donation))

print("Done. {} records processed.".format(len(donations)))
