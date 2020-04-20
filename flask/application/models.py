from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from application import db, login_manager
from flask_login import UserMixin
import secrets


@login_manager.user_loader
def load_user(hospital_id):
    return Hospital.query.get(int(hospital_id))


class Hospital(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(20), unique=True, nullable=False)
    address = db.Column(db.String(), nullable=False)
    state = db.Column(db.String(), nullable=False)
    hex_id = db.Column(db.String(), nullable=False)

    email = db.Column(db.String(120), unique=True, nullable=True)
    password = db.Column(db.String(60), nullable=True)

    data = db.relationship('Data', backref='hospital', lazy=True)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'hospital_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            hospital_id = s.loads(token)['hospital_id']
        except:
            return None
        return Hospital.query.get(hospital_id)

    def __repr__(self):
        return f"Hospital('{self.id}', '{self.name}', '{self.state}')"


class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    bed_capacity = db.Column(db.Integer(), nullable=False)
    beds_available = db.Column(db.Integer(), nullable=False)
    icus_available = db.Column(db.Integer(), nullable=False)
    ventilators_available = db.Column(db.Integer(), nullable=False)
    coronavirus_tests_available = db.Column(db.Integer(), nullable=False)
    coronavirus_patients = db.Column(db.Integer(), nullable=False)
    hospital_id = db.Column(db.Integer, db.ForeignKey('hospital.id'), nullable=False)

    def __repr__(self):
        return f"Data('{self.hospital_id}', '{self.date}')"
