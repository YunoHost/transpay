from sqlalchemy import Column, Integer, String, Unicode, Boolean, DateTime
from sqlalchemy import ForeignKey, Table, UnicodeText, Text, text
from sqlalchemy.orm import relationship, backref
from .database import Base

from datetime import datetime
import bcrypt
import os
import hashlib

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key = True)
    email = Column(String(256), nullable = False, index = True)
    admin = Column(Boolean())
    password = Column(String)
    created = Column(DateTime)
    passwordReset = Column(String(128))
    passwordResetExpiry = Column(DateTime)

    def set_password(self, password):
        self.password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    def __init__(self, email, password):
        self.email = email
        self.admin = False
        self.created = datetime.now()
        self.set_password(password)

    def __repr__(self):
        return '<User %r>' % self.username

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
