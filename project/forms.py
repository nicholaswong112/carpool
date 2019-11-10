from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, SubmitField, TextAreaField, DateField, IntegerField
from wtforms.validators import ValidationError, DataRequired, EqualTo, Length, NumberRange
from project.models import Ministry, Ride, Passenger


class CreateMinistryForm(FlaskForm):
    ministry_name = StringField('Ministry Name')#, validators=[DataRequired(), Length(max=30)])
    submit = SubmitField('Create Ministry')


# Figure out whether this should route to Ministrylogin
class FindMinistryForm(FlaskForm):
    ministry_id = StringField('Ministry Code', validators=[DataRequired()])
    submit = SubmitField('Find Ministry')


class RideSearchForm(FlaskForm):
    date = DateField('Date', validators=[DataRequired()])
    submit = SubmitField('Search')
    # TODO modify destination based on what is in the sql db


class DriverSubmitForm(FlaskForm):
    submit = SubmitField('I want to be a driver!')


class DriverSignupForm(FlaskForm):
    driver_name = StringField('Name', validators=[DataRequired(), Length(max=30)])
    driver_addr = StringField('Driver Address', validators=[DataRequired()])
    driver_phone = StringField('Driver Phone Number', validators=[DataRequired(), Length(max=30)])
    date = DateField('Date (YYYY-MM-DD)', validators=[DataRequired()])
    time = StringField('Time', validators=[DataRequired(), Length(max=30)])
    dest = StringField('Destination', validators=[DataRequired()])
    open_seats = IntegerField('Open Seats', validators=[DataRequired(), NumberRange(min=1)])
    submit = SubmitField('Sign Up')


class RideDisplayForm(FlaskForm):
    ride_details = SelectField('Ride details', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Sign Up')


class PassengerSignupForm(FlaskForm):
    passenger_name = StringField('Name', validators=[DataRequired(), Length(max=30)])
    passenger_phone = StringField('Contact Info', validators=[DataRequired(), Length(max=30)])
    passenger_addr = StringField('Pickup Address', validators=[DataRequired(), Length(max=30)])
    submit = SubmitField('Sign Up')
