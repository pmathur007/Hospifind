from flask_wtf import FlaskForm
from wtforms import IntegerField, SelectField, SubmitField
from wtforms.validators import DataRequired, ValidationError, NumberRange

class ReportWaitTimeForm(FlaskForm):
    testing_center = SelectField('Testing Center', coerce=int, choices=[], default=0, validators=[DataRequired()])
    hours = IntegerField('Hours', validators=[DataRequired()])
    minutes = IntegerField('Minutes', validators=[DataRequired(), NumberRange(0, 59)])
    submit = SubmitField('Report Wait Time')

    def validate_testing_center(self, testing_center):
        if testing_center == 0:
            raise ValidationError("Please select a testing center.")