from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, NumberRange
from flask_login import current_user


class GovernmentRequestAccountForm(FlaskForm):
    government = StringField('Government Name', validators=[DataRequired()])
    government_type = StringField(
        'Government Type (City, County, State, etc.)', validators=[DataRequired()])
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


class GovernmentRegistrationForm(FlaskForm):
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
