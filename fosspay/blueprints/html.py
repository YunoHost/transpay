from flask import Blueprint, render_template, abort, request, redirect, session, url_for, send_file, Response
from flask.ext.login import current_user, login_user, logout_user
from datetime import datetime, timedelta
from fosspay.objects import *
from fosspay.database import db
from fosspay.common import *
from fosspay.config import _cfg, load_config

import os
import locale
import bcrypt
import hashlib
import stripe
import binascii

encoding = locale.getdefaultlocale()[1]
html = Blueprint('html', __name__, template_folder='../../templates')

@html.route("/")
def index():
    if User.query.count() == 0:
        load_config()
        return render_template("setup.html")
    projects = sorted(Project.query.all(), key=lambda p: p.name)
    avatar = "//www.gravatar.com/avatar/" + hashlib.md5(_cfg("your-email").encode("utf-8")).hexdigest()
    selected_project = request.args.get("project")
    if selected_project:
        try:
            selected_project = int(selected_project)
        except:
            selected_project = None
    return render_template("index.html", projects=projects,
            avatar=avatar, selected_project=selected_project)

@html.route("/setup", methods=["POST"])
def setup():
    if not User.query.count() == 0:
        abort(400)
    email = request.form.get("email")
    password = request.form.get("password")
    if not email or not password:
        return redirect("/") # TODO: Tell them what they did wrong (i.e. being stupid)
    user = User(email, password)
    user.admin = True
    db.add(user)
    db.commit()
    login_user(user)
    return redirect("/admin?first-run=1")

@html.route("/admin")
@adminrequired
def admin():
    first = request.args.get("first-run") is not None
    projects = Project.query.all()
    unspecified = Donation.query.filter(Donation.project == None).all()
    donations = Donation.query.order_by(Donation.created.desc()).limit(50).all()
    return render_template("admin.html",
        first=first,
        projects=projects,
        donations=donations,
        one_times=lambda p: sum([d.amount for d in p.donations if d.type == DonationType.one_time]),
        recurring=lambda p: sum([d.amount for d in p.donations if d.type == DonationType.monthly]),
        unspecified_one_times=sum([d.amount for d in unspecified if d.type == DonationType.one_time]),
        unspecified_recurring=sum([d.amount for d in unspecified if d.type == DonationType.monthly])
    )

@html.route("/create-project", methods=["POST"])
@adminrequired
def create_project():
    name = request.form.get("name")
    project = Project(name)
    db.add(project)
    db.commit()
    return redirect("/admin")

@html.route("/login", methods=["GET", "POST"])
def login():
    if current_user:
        if current_user.admin:
            return redirect("/admin")
        return redirect("/panel")
    if request.method == "GET":
        return render_template("login.html")
    email = request.form.get("email")
    password = request.form.get("password")
    if not email or not password:
        return render_template("login.html", errors=True)
    user = User.query.filter(User.email == email).first()
    if not user:
        return render_template("login.html", errors=True)
    if not bcrypt.hashpw(password.encode('UTF-8'), user.password.encode('UTF-8')) == user.password.encode('UTF-8'):
        return render_template("login.html", errors=True)
    login_user(user)
    if user.admin:
        return redirect("/admin")
    return redirect("/panel")

@html.route("/logout")
@loginrequired
def logout():
    logout_user()
    return redirect("/")

@html.route("/donate", methods=["POST"])
@json_output
def donate():
    email = request.form.get("email")
    stripe_token = request.form.get("stripe_token")
    amount = request.form.get("amount")
    type = request.form.get("type")
    comment = request.form.get("comment")
    project_id = request.form.get("project")

    # validate and rejigger the form inputs
    if not email or not stripe_token or not amount or not type:
        return { "success": False, "reason": "Invalid request" }, 400
    try:
        if project_id is None or project_id == "null":
            project = None
        else:
            project_id = int(project_id)
            project = Project.query.filter(Project.id == project_id).first()

        if type == "once":
            type = DonationType.one_time
        else:
            type = DonationType.monthly
    except:
        return { "success": False, "reason": "Invalid request" }, 400

    new_account = False
    user = User.query.filter(User.email == email).first()
    if not user:
        new_account = True
        user = User(email, binascii.b2a_hex(os.urandom(20)).decode("utf-8"))
        user.password_reset = binascii.b2a_hex(os.urandom(20)).decode("utf-8")
        user.password_reset_expires = datetime.now() + timedelta(days=1)
        customer = stripe.Customer.create(email=user.email, card=stripe_token)
        user.stripe_customer = customer.id
        db.add(user)
    else:
        customer = stripe.Customer.retrieve(user.stripe_customer)
        new_source = customer.sources.create(source=stripe_token)
        customer.default_source = new_source.id
        customer.save()

    donation = Donation(user, type, amount, project, comment)
    db.add(donation)

    try:
        charge = stripe.Charge.create(
            amount=amount,
            currency="usd",
            customer=user.stripe_customer,
            description="Donation to " + _cfg("your-name")
        )
    except stripe.error.CardError as e:
        db.rollback()
        db.close()
        return { "success": False, "reason": "Your card was declined." }

    db.commit()

    if new_account:
        return { "success": True, "new_account": new_account, "password_reset": user.password_reset }
    else:
        return { "success": True, "new_account": new_account }

@html.route("/password-reset", methods=['GET', 'POST'], defaults={'token': None})
@html.route("/password-reset/<token>", methods=['GET', 'POST'])
def reset_password(token):
    if not token and request.method == "POST":
        token = request.form.get("token")
        if not token:
            redirect("/")
    else:
        redirect("/")
    user = User.query.filter(User.password_reset == token).first()
    if not user:
        redirect("/")
    if request.method == 'GET':
        if user.password_reset_expires == None or user.password_reset_expires < datetime.now():
            return render_template("reset.html", expired=True)
        if user.password_reset != token:
            redirect("/")
        return render_template("reset.html", token=token)
    else:
        if user.password_reset_expires == None or user.password_reset_expires < datetime.now():
            abort(401)
        if user.password_reset != token:
            abort(401)
        password = request.form.get('password')
        if not password:
            return render_template("reset.html", token=token, errors="You need to type a new password.")
        user.set_password(password)
        user.password_reset = None
        user.password_reset_expires = None
        db.commit()
        login_user(user)
        return redirect("/panel")

@html.route("/panel")
@loginrequired
def panel():
    return render_template("panel.html",
        one_times=lambda u: [d for d in u.donations if d.type == DonationType.one_time],
        recurring=lambda u: next(d for d in u.donations if d.type == DonationType.recurring))
