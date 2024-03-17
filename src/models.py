import sqlalchemy as sa 
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker, relationship, backref 

engine = sa.create_engine("sqlite:///:memory:")
session = scoped_session(sessionmaker(bind=engine))
Base = declarative_base()

from . import db

class User(db.Model):
    __tablename__ = "users"
    id = sa.Column(sa.Integer, primary_key=True)
    firstname = sa.Column(sa.String, nullable=False)
    lastname = sa.Column(sa.String, nullable=False)
    email = sa.Column(sa.String, nullable=False, unique=True)
    isProvider = sa.Column(sa.Boolean, default=False, nullable=False)
    password = sa.Column(sa.String, nullable=False)

class Appointment(db.Model):
    __tablename__ = "appointments"
    id = sa.Column(sa.Integer, primary_key=True)
    starttime = sa.Column(sa.TIMESTAMP)
    provider_id = sa.Column(sa.Integer, sa.ForeignKey("users.id"), nullable=False)
    client_id = sa.Column(sa.Integer, sa.ForeignKey("users.id"))
    isConfirmed = sa.Column(sa.Boolean, default=False, nullable=False)
