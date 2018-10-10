from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from .config import _cfg, _cfgi
from sqlite3 import dbapi2 as sqlite

engine = create_engine(_cfg('connection-string'), module=sqlite)

db = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()
Base.query = db.query_property()

def init_db():
    import core.objects
    Base.metadata.create_all(bind=engine)
