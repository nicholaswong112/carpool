from flask import render_template, flash, redirect, url_for, request
from project import app, db
from project.forms import CreateRoomForm, FindRoomForm, RideSearchForm, DriverSubmitForm, DriverSignupForm, \
    PassengerSignupForm
from project.models import User, Room, List
import random
import string


@app.route('/')
@app.route('/home')
def index():
    return render_template('index.html', title='Home')


@app.route('/findroom', methods=['GET', 'POST'])
def find_room():
    form = FindRoomForm()
    if form.validate_on_submit():
        current_room = Room.query.filter_by(room_id=form.room_id.data).first()
        if current_room is None:
            flash('Room not found.')
            return redirect(url_for('find_room'))
        else:
            return redirect(url_for('room', room_id=form.room_id.data))
    return render_template('find-room.html', title='Find Your Ministry', form=form)


@app.route('/createroom', methods=['GET', 'POST'])
def create_room():
    form = CreateRoomForm()
    if form.validate_on_submit():
        room_id = generate_rand_room_id()  # TODO look at this after db ready

        while Room.query.filter_by(room_id=room_id).first() is not None:
            room_id = generate_rand_room_id()

        new_room = Room(room_id=room_id, room_name=form.room_name.data, password_required=form.password_required.data)
        db.session.add(new_room)
        if form.password_required.data:
            new_room.set_password(form.password.data)
        db.session.commit()

        return redirect(url_for('room', room_id=room_id))
    else:
        form.room_name.data = "Ministry Room"
    return render_template('create-room.html', title='Create Room', form=form)


def generate_rand_room_id():
    return ''.join([random.choice(string.ascii_lowercase) for i in range(5)])


@app.route('/room/<room_id>')
def room(room_id):
    ride_form = RideSearchForm()
    if ride_form.validate_on_submit():
        ride_hash = ride_form.date.data

        return redirect(url_for('room'), room_id=room_id, event_id=ride_hash)

    driver_form = DriverSubmitForm()
    if driver_form.validate_on_submit():
        return redirect(url_for('driver'), room_id=room_id)

    room = Room.query.filter_by(room_id=room_id).first()

    if room is None:
        return redirect(url_for('create_room'))
    # TODO Add a form for selecting the date and destination of the cars
    # TODO Probably need to add all of the destinations available to the user

    return render_template('room.html', room=room, ride_form=ride_form, driver_form=driver_form)


@app.route('/driver/<room_id>')
def driver_signup(room_id):
    form = DriverSignupForm
    if form.validate_on_submit():
        driver_name = form.driver_name.data
        date = form.date.data
        dest = form.destination.data
        contact = form.contact.data
        open_seats = form.open_seats.data

        # TODO Take the form data and put it in the database
        return redirect(url_for('room'), room_id=room_id)

    return render_template('driver_signup.html', form=form)


@app.route('/room/<room_id>/<event_id>')
def event(room_id, event_id):
    room = Room.query.filter_by(room_id=room_id).first()

    if room is None:
        return redirect(url_for('create_room'))

    event = None
    # TODO parse the event to generate all of the cars that are available.

    # TODO display the cars in some sort of form.

    return render_template('car_select.html', room=room)
