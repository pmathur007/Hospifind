from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, NumberRange
from flask_login import current_user
from application.models import User


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
