from fosspay.config import _cfg

import stripe

if _cfg("stripe-secret") != "":
    stripe.api_key = _cfg("stripe-secret")
