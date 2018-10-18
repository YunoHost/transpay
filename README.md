# Trans Pay [![Donate with Trans Pay](https://transpay.xn--transposes-i7a.eu/static/donate-with-transpay.png)](https://dons.transposées.eu/)

Trans Pay is developed by [Collectif Trans Posé·e·s](https://transposées.eu) for our own use and that of other associations.

This tool is used to receive and manage donations:

* Supports one-time and monthly donations
* Process cards with Stripe
* Flexible and customizable

It works for individuals and it works for organizations. Expect to
spend about an hour or two setting up everything and then you're good to go.

Test instance if you want to see how donating works : https://transpay.transposées.eu/

For support, file an issue.

Changelog : https://gitlab.kokakiwi.net/transposees/transpay/tags

## Before you start

You will need a number of things set up before you start:

1. An approved [Stripe](https://stripe.com/) account
1. A mail server
1. A domain name and an SSL certificate
1. A web server to host Trans Pay on

## Installation

For installation instructions, see our [wiki](https://gitlab.kokakiwi.net/transposees/transpay/wikis/home).

## Deployment

Once you have everything configured, you will need to switch from the dev server
into something more permanent. Install gunicorn on your server and use the
systemd unit provided in `contrib/`. You will also probably want to run this
through nginx instead of directly exposing gunicorn to the web, see
`contrib/nginx.conf`. Neither the nginx configuration or the systemd unit are
immediately ready to use - read them and change them to suit your needs.

Using nginx or something like it is necessary for SSL support, and you must
serve your site with https for Stripe to work.
