from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from application import db, login_manager
from flask_login import UserMixin
from os import urandom
import copy

class Hospital(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String, nullable=False)
    address = db.Column(db.String, nullable=False)
    state = db.Column(db.String, nullable=False)
    county = db.Column(db.String, nullable=False)
    latitude = db.Column(db.Integer, nullable=True)
    longitude = db.Column(db.Integer, nullable=True)
    data = db.Column(db.JSON, nullable=True)
    # timeSubmitted: DateTime
    # bedsAvailable: Integer
    # icusAvailable: Integer

    def __repr__(self):
        return "Hospital('" + str(self.id) + "', '" + self.name + "', '" + self.state + "')"

class TestingCenter(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String, nullable=False)
    address = db.Column(db.String, nullable=False)
    state = db.Column(db.String, nullable=False)
    county = db.Column(db.String, nullable=False)
    latitude = db.Column(db.Integer, nullable=True)
    longitude = db.Column(db.Integer, nullable=True)

    hours = db.Column(db.JSON, nullable=False)
    # day of week: [hours]

    walkUp = db.Column(db.Boolean, nullable=True)
    referral = db.Column(db.Boolean, nullable=True)
    appointment = db.Column(db.Boolean, nullable=True)
    info = db.Column(db.String, nullable=True)

    data = db.Column(db.JSON, nullable=True)
    # [{wait time, time submitted, submission_ip}]

class Submission(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    ip = db.Column(db.String, nullable=False)
    submission_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    testing_center_name = db.Column(String, nullable=False)