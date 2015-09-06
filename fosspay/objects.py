from sqlalchemy import Column, Integer, String, Unicode, Boolean, DateTime
from sqlalchemy import ForeignKey, Table, UnicodeText, Text, text
from sqlalchemy.orm import relationship, backref
from sqlalchemy_utils import ChoiceType

from .database import Base

from datetime import datetime
from enum import Enum
import bcrypt
import os
import hashlib

class DonationType(Enum):
    one_time = "one_time"
    monthly = "monthly"

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String(256), nullable=False, index=True)
    admin = Column(Boolean())
    password = Column(String)
    created = Column(DateTime)
    password_reset = Column(String(128))
    password_reset_expires = Column(DateTime)
    stripe_customer = Column(String(256))

    def set_password(self, password):
        self.password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    def __init__(self, email, password):
        self.email = email
        self.admin = False
        self.created = datetime.now()
        self.set_password(password)

    def __repr__(self):
        return "<User {}>".format(self.email)

    # Flask.Login stuff
    # We don't use most of these features
    def is_authenticated(self):
        return True
    def is_active(self):
        return True
    def is_anonymous(self):
        return False
    def get_id(self):
        return self.email

class Donation(Base):
    __tablename__ = 'donations'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("User", backref=backref("donations"))
    project_id = Column(Integer, ForeignKey("projects.id"))
    project = relationship("Project", backref=backref("donations"))
    type = Column(ChoiceType(DonationType, impl=String()))
    amount = Column(Integer, nullable=False)
    created = Column(DateTime, nullable=False)
    emailed_about = Column(Boolean, nullable=False)

    def __init__(self, user, type, amount, project=None):
        self.user = user
        self.type = type
        self.amount = amount
        self.created = datetime.now()
        self.emailed_about = False
        self.project = project

    def __repr__(self):
        return "<Donation {} from {}: ${} ({})>".format(
                self.id,
                self.user.email,
                self.amount,
                self.type
            )

class Project(Base):
    __tablename__ = 'projects'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    created = Column(DateTime, nullable=False)

    def __init__(self, name):
        self.name = name
        self.created = datetime.now()

    def __repr__(self):
        return "<Project {} {}>".format(self.id, self.name)
