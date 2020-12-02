from flask_wtf import FlaskForm
from wtforms import StringField, DateField, DateTimeField, IntegerField, SubmitField, DecimalField, TimeField
from wtforms.validators import DataRequired, Email


class UserForm(FlaskForm):
    first_name = StringField('first_name', validators=[DataRequired("First name is required.")])
    last_name = StringField('last_name', validators=[DataRequired("Last name is required.")])
    birthdate = DateField('birthdate', validators=[DataRequired("Birthdate is required.")])
    email = StringField('email', validators=[Email("Incorrect email format."), DateField("Email is required.")])
    submit = SubmitField('submit')


class ReadingForm(FlaskForm):
    weight = IntegerField('weight', validators=[DataRequired('Weight is required')])
    blood_pressure = IntegerField('blood_pressure', validators=[DataRequired('Blood pressure is required.')])
    temperature = IntegerField('temperature', validators=[DataRequired('Temperature is required.')])
    oxygen_level = DecimalField('oxygen_level', validators=[DataRequired('Oxygen level is required.')])
    pulse = IntegerField('pulse', validators=[DataRequired('Pulse is required.')])
    timestamp = DateTimeField('timestamp', validators=[DataRequired('Timestamp is required.')])
    submit = SubmitField('submit')


class ActivityForm(FlaskForm):
    type = StringField('type', validators=[DataRequired('Type is required.')])
    description = StringField('description', validators=[DataRequired('Description is required.')])
    start_time = DateTimeField('start_time', validators=[DataRequired('Start time is required.')])
    end_time = DateTimeField('end_time', validators=[DataRequired('End time is required.')])
    submit = SubmitField('submit')