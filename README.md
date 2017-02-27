# fosspay [![Donate with fosspay](https://drewdevault.com/donate/static/donate-with-fosspay.png)](https://drewdevault.com/donate?project=3)

Donation collection for FOSS groups and individuals.

For support, visit [#cmpwn on
irc.freenode.net](http://webchat.freenode.net/?channels=cmpwn&uio=d4)
or file a GitHub issue.

## Rationale

Getting paid to write open source is *hard*. There are several problems with
donations:

* No job security
* Not likely to be enough to switch to full time
* Without being full time, it's hard to be productive

Some projects get support from companies, but most projects are not on the right
scale for that to happen, and some projects (like most of my own) do not provide
business value and wouldn't get sponsored regardless of size.

So, the solution: keep your job, and collect donations until you have raised
enough to support one week of full time development on your open source
projects. Take a week of unpaid leave and get some FOSS shit done.

## fosspay

This software will collect donations for you. Want to take it for a test drive?
[Send me a buck](https://drewdevault.com/donate?project=3).

* Supports one-time and monthly donations
* Process cards with Stripe - also supports Bitcoin
* Flexible and customizable

It works for individuals (like me) and it works for organizations. Expect to
spend about an hour or two setting up everything and then you're good to go.

## Before you start

Do these things first:

1. Research the tax implications for your country
1. Speak with your employer about it

You will need a number of things set up before you start:

1. An approved [Stripe](https://stripe.com/) account
1. A mail server (try [Mandrill](http://mandrill.com/) if you don't have one)
1. A domain name and an SSL certificate (try [Namecheap](http://www.namecheap.com/?aff=84838) and [StartSSL](http://www.startssl.com/))
1. A web server to host fosspay on (try [Linode](http://linode.com/) if you don't have one)

## Installation

Install these things:

* Python 3
* pip (python 3)
* PostgreSQL

You're responsible for setting up PostgreSQL yourself. Prepare a connection
string for later.

Clone the git repository on the server that you want to host fosspay on:

    git clone git://github.com/SirCmpwn/fosspay.git
    cd fosspay

Install the Python packages:

    sudo pip3 install -r requirements.txt

Compile the static assets:

    make

Create a configuration file:

    cp config.ini.example config.ini

Edit `config.ini` to your liking. Then, you can run the following to start up
the development server:

    python3 app.py

Log into http://your-domain:5000, and you will receive further instructions.

## Deployment

Once you have everything configured, you will need to switch from the dev server
into something more permanent. Install gunicorn on your server and use the
systemd unit provided in `contrib/`. You will also probably want to run this
through nginx instead of directly exposing gunicorn to the web, see
`contrib/nginx.conf`. Neither the nginx configuration or the systemd unit are
immediately ready to use - read them and change them to suit your needs.

Using nginx or something like it is necessary for SSL support, and you must
serve your site with https for Stripe to work.
