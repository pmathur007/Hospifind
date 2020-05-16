from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, NumberRange
from flask_login import current_user
from application.models import User


class RegistrationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    username = StringField('Username', validators=[
                           DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[
                                     DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError(
                'That username is taken. Please choose a different one!')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError(
                'That email is already registered. Please choose a different one or contact us if you think this is a mistake!')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class DataForm(FlaskForm):
    bed_capacity = IntegerField('Total Beds', validators=[
                                DataRequired(), NumberRange(0, 10000)])
    beds_available = IntegerField('Beds Available', validators=[
                                  DataRequired(), NumberRange(0, 10000)])
    icus_available = IntegerField('ICUs Available', validators=[
                                  DataRequired(), NumberRange(0, 10000)])
    ventilators_available = IntegerField('Ventilators Available', validators=[
                                         DataRequired(), NumberRange(0, 10000)])
    coronavirus_tests_available = IntegerField('Coronavirus Tests Available (or Daily Average)', validators=[
                                               DataRequired(), NumberRange(0, 10000)])
    coronavirus_patients = IntegerField('Coronavirus Patients', validators=[
                                        DataRequired(), NumberRange(0, 10000)])
    submit = SubmitField('Submit')


class UpdateAccountForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    username = StringField('Username', validators=[
                           DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Update Account')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError(
                    'That username is taken. Please choose a different one!')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError(
                    'That email is taken. Please choose a different one!')


class HospitalRequestAccountForm(FlaskForm):
    hospital = StringField('Hospital Name', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    title = StringField('Title', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone Number', validators=[DataRequired()])
    message = TextAreaField('Message/Additional Details')
    submit = SubmitField('Submit Request')

    def validate_phone(self, phone):
        if len(phone.data) < 10 or len(phone.data) > 15:
            raise ValidationError('Please enter a valid phone number.')
        for char in phone.data:
            if char not in '0123456789-+':
                raise ValidationError('Please enter a valid phone number.')


class RequestPasswordResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError(
                'There is no account with that email. You must register first.')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[
                                     DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')
