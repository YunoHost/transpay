# fosspay

Helps you get paid for your open source work.

[![](https://img.shields.io/badge/Donations-fosspay-brightgreen.svg)](https://drewdevault.com/donate)

## Rationale

I write a ton of open source software, but almost none of it is on the scale
that I can expect reliable income from donations, or the sorts of projects that
a business would be likely to fund. It's very unlikely that I'd receive enough
donations from random folks to support full time open source work, but full time
is the best way to make serious progress on your projects.

So - here's how this works: supporters give you one-time or recurring donations,
and after a while you get enough to take a week off from work to spend on open
source work. Since I have several projects, I also ask supporters to tell me
what project they're donating towards, and I distribute the load based on which
projects receive the most support.

## Before you start

Talk to your employer. The way that this is designed to work is that you
continue working full-time at your job, and collect donations. After a while,
you should have enough donations to take some period of unpaid leave - a week, a
month, or whatever works.

* You keep your current job and job security
* You get paid to work on FOSS even with flaky or inconsistent donations
* Everyone wins

There are a few things you need to talk about with your employer:

1. Make sure you own the IP for the things you write during your open source
    sprints.
1. Make sure that you have a job to come back to afterwards.
1. Research the tax implications of accepting these donations.

### Stripe

Payments are taken through Stripe, which is pretty headache-free for you to use.
You need to set up an approved Stripe account, which you can get from here:

https://stripe.com/

### Mandrill

You will need a mail server of some sort. If you don't want to go through the
trouble of setting one up, you can use Mandrill:

http://mandrill.com/

You can probably also use your existing mail server, which is what I do, which
makes it easy for people to email you questions and such.

### SSL

You will need an SSL certificate for your website (you also need a domain name).
You can get a free SSL certificate from [StartSSL](http://www.startssl.com/),
but they've always felt pretty... bad to me. You can pay for one instead at
[RapidSSL](https://www.rapidssl.com/), which is what I use personally. You can
also get one for free from [Let's Encrypt](https://letsencrypt.org/) if that
ever happens.

If you need a domain, you can use my referral link for
[Namecheap](http://www.namecheap.com/?aff=84838) and that'd be super nice of
you. Here's a link to Namecheap without the referral link:
[Namecheap](http://www.namecheap.com).

## Installation

Install these things (Arch Linux packages in parenthesis):

* Python 3 (python)
* PostgreSQL (postgresql)
* scss (ruby-sass)
* Flask (python-flask)
* SQLAlchemy (python-sqlalchemy)
* Flask-Login (python-flask-login)
* psycopg2 (python-psycopg2)
* bcrypt (python-bcrypt)

You'll have to configure PostgreSQL yourself and get a connection string that
fosspay can use. Then you can clone this repository to wherever you want to run
it from (I suggest making an unprivledged user account on the server you want to
host this on).

### Configuration

Copy config.ini.example to config.ini and edit it to your liking. Then, you can
run this command to try the site in development mode:

    python app.py

[Click here](http://localhost:5000) to visit your donation site and further
instructions will be provided there.

### Static Assets

Run `make` to compile static assets.

### Production Deployment

To deploy this to production, copy the systemd unit from `contrib/` to your
server at `/etc/systemd/system/` (or whatever's appropriate for your distro).
Use `sytsemctl enable fosspay` and `systemctl start fosspay` to run the site on
`127.0.0.1:8000` (you can change this port by editing the unit file). You should
configure nginx to proxy through to fosspay from whatever other website you
already have. My nginx config is provided in `contrib/` for you to take a look
at - it proxies most requests to Github pages (my blog), and `/donate` to
fosspay.
