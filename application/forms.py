from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, NumberRange
from flask_login import current_user
from application.models import User


class RegistrationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one!')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is already registered. Please choose a different one or contact us if you think this is a mistake!')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class DataForm(FlaskForm):
    bed_capacity = IntegerField('Total Beds', validators=[DataRequired(), NumberRange(0, 10000)])
    beds_available = IntegerField('Beds Available', validators=[DataRequired(), NumberRange(0, 10000)])
    icus_available = IntegerField('ICUs Available', validators=[DataRequired(), NumberRange(0, 10000)])
    ventilators_available = IntegerField('Ventilators Available', validators=[DataRequired(), NumberRange(0, 10000)])
    coronavirus_tests_available = IntegerField('Coronavirus Tests Available (or Daily Average)', validators=[DataRequired(), NumberRange(0, 10000)])
    coronavirus_patients = IntegerField('Coronavirus Patients', validators=[DataRequired(), NumberRange(0, 10000)])
    submit = SubmitField('Submit')


class HospitalNameForm(FlaskForm):
    hospital_name = StringField('Hospital Name', validators=[DataRequired()])
    submit = SubmitField('Request Account')


class PatientForm(FlaskForm):
    pass


class UpdateAccountForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Update Account')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one!')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one!')
