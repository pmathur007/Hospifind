from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, NumberRange
from flask_login import current_user
from application.models import User


class InputLocationForm(FlaskForm):
    street_address = StringField('Street Address')
    city = StringField('City')
    state = StringField('State')
    country = StringField('Country')
    zip_code = StringField('Zip Code')
    submit = SubmitField('Update Location')
