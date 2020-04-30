from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from application import db, login_manager
from flask_login import UserMixin
from os import urandom
import copy


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Hospital(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String, nullable=False)
    address = db.Column(db.String, nullable=False)
    state = db.Column(db.String, nullable=False)
    latitude = db.Column(db.Integer, nullable=True)
    longitude = db.Column(db.Integer, nullable=True)
    admin_hex_id = db.Column(db.String, default=lambda: urandom(32).hex(), unique=True, nullable=True)
    normal_hex_id = db.Column(db.String, default=lambda: urandom(32).hex(), unique=True, nullable=True)
    system_open = db.Column(db.Boolean, default=True)
    old_admin_hex_id = db.Column(db.String, default=None, nullable=True)
    old_normal_hex_id = db.Column(db.String, default=None, nullable=True)

    data = db.relationship('Data', backref='input', lazy=True)

    # def get_reset_token(self, expires_sec=1800):
    #     s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
    #     return s.dumps({'hospital_id': self.id}).decode('utf-8')
    #
    # @staticmethod
    # def verify_reset_token(token):
    #     s = Serializer(current_app.config['SECRET_KEY'])
    #     try:
    #         hospital_id = s.loads(token)['hospital_id']
    #     except:
    #         return None
    #     return Hospital.query.get(hospital_id)

    def regenerate_hex_ids(self):
        self.admin_hex_id = urandom(32).hex()
        self.normal_hex_id = urandom(32).hex()

    def close_system(self):
        self.old_admin_hex_id = copy.deepcopy(self.admin_hex_id)
        self.old_normal_hex_id = copy.deepcopy(self.normal_hex_id)
        self.admin_hex_id = None
        self.normal_hex_id = None
        self.system_open = False

    def open_system(self):
        self.admin_hex_id = self.old_admin_hex_id
        self.normal_hex_id = self.old_normal_hex_id
        self.system_open = True

    def __repr__(self):
        return "Hospital('" + str(self.id) + "', '" + self.name + "', '" + self.state + "')"


class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)

    name = db.Column(db.String, nullable=False)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False)
    password = db.Column(db.String, nullable=False)
    hospital = db.Column(db.Integer, db.ForeignKey('hospital.id'), nullable=False)

    def __repr__(self):
        return "User('" + self.username + "', '" + self.hospital + "')"


class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    bed_capacity = db.Column(db.Integer, nullable=False)
    beds_available = db.Column(db.Integer, nullable=False)
    icus_available = db.Column(db.Integer, nullable=False)
    ventilators_available = db.Column(db.Integer, nullable=False)
    coronavirus_tests_available = db.Column(db.Integer, nullable=False)
    coronavirus_patients = db.Column(db.Integer, nullable=False)
    coronavirus_patient_percent = db.Column(db.Float, nullable=False)
    user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    hospital = db.Column(db.Integer, db.ForeignKey('hospital.id'), nullable=False)

    def __repr__(self):
        return "Data('" + self.hospital + "', '" + self.user + "', '" + self.date + "')"
        #f"Data(Hospital: '{self.hospital}', User: '{self.user}', Date: '{self.date}') \nBed Capacity:{self.bed_capacity}\nBeds Available: {self.beds_available}\nICUs Available: {self.icus_available}\nVentilators Available: {self.ventilators_available}\nCoronavirus Tests Available: {self.coronavirus_tests_available}\nCoronavirus Patients: {self.coronavirus_patients}\nCoronavirus Patient Percent: {self.coronavirus_patient_percent}'"
