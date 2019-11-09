from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, SubmitField, TextAreaField, DateField, IntegerField
from wtforms.validators import ValidationError, DataRequired, EqualTo, Length, NumberRange
from project.models import User, Song, Room, List


class CreateRoomForm(FlaskForm):
    room_name = StringField('Room Name', validators=[DataRequired(), Length(max=30)])
    submit = SubmitField('Create Room')


# Figure out whether this should route to roomlogin
class FindRoomForm(FlaskForm):
    room_id = StringField('Room Code', validators=[DataRequired()])
    submit = SubmitField('Find Room')


class RideSearchForm(FlaskForm):
    date = DateField('Date', validators=[DataRequired()])
    submit = SubmitField('Search')
    # TODO modify destination based on what is in the sql db


class DriverSubmitForm(FlaskForm):
    submit = SubmitField('I want to be a driver!')


class DriverSignupForm(FlaskForm):
    driver_name = StringField('Name', validators=[DataRequired(), Length(max=30)])
    date = DateField('Date', validators=[DataRequired()])
    time = StringField('Time', validators=[DataRequired(), Length(max=30)])
    destination = TextAreaField('Destination', validators=[DataRequired()])
    contact = StringField('Contact Info', validators=[DataRequired(), Length(max=30)])
    open_seats = IntegerField('Open Seats', validators[DataRequired(), NumberRange(min=1)])
    submit = SubmitField('Sign Up')


class PassengerSignupForm(FlaskForm):
    passenger_name = StringField('Name', validators=[DataRequired(), Length(max=30)])
    contact = StringField('Contact Info', validators=[DataRequired(), Length(max=30)])
    pickup = StringField('Pickup Address', validators=[DataRequired(), Length(max=30)])
    submit = SubmitField('Sign Up')
