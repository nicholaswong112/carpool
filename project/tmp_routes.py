from flask import render_template, flash, redirect, url_for, request
from project import app, db
from project.forms import CreateMinistryForm, FindMinistryForm, RideSearchForm, DriverSubmitForm, DriverSignupForm, \
    PassengerSignupForm
from project.models import Ministry, Ride, Passenger
import random
import string


@app.route('/')
@app.route('/home')
def index():
    return render_template('index.html', title='Home')


@app.route('/findministry', methods=['GET', 'POST'])
def find_ministry():
    form = FindMinistryForm()
    if form.validate_on_submit():
        current_ministry = Ministry.query.filter_by(ministry_id=form.ministry_id.data).first()
        if current_ministry is None:
            flash('Ministry not found.')
            return redirect(url_for('findministry'))
        else:
            return redirect(url_for('ministry', ministry_id=form.ministry.data))
    return render_template('find-ministry.html', title='Find Your Ministry', form=form)


@app.route('/createministry', methods=['GET', 'POST'])
def create_ministry():
    form = CreateMinistryForm()
    if form.validate_on_submit():
        ministry_id = generate_rand_ministry_id()  # TODO look at this after db ready

        while Ministry.query.filter_by(ministry_id=ministry_id).first() is not None:
            ministry_id = generate_rand_ministry_id()

        new_ministry = Ministry(ministry_id=ministry_id, ministry_name=form.ministry_name.data, password_required=form.password_required.data)
        db.session.add(new_ministry)
        if form.password_required.data:
            new_ministry.set_password(form.password.data)
        db.session.commit()

        return redirect(url_for('ministry', ministry_id=ministry_id))
    else:
        form.ministry_name.data = "Ministry Ministry"
    return render_template('create-ministry.html', title='Create ministry', form=form)


def generate_rand_ministry_id():
    return ''.join([random.choice(string.ascii_lowercase) for i in range(5)])


@app.route('/ministry/<ministry_id>')
def ministry(ministry_id):
    ride_form = RideSearchForm()
    if ride_form.validate_on_submit():
        ride_hash = ride_form.date.data

        return redirect(url_for('ministry'), ministry_id=ministry_id, event_id=ride_hash)

    driver_form = DriverSubmitForm()
    if driver_form.validate_on_submit():
        return redirect(url_for('driver'), ministry_id=ministry_id)

    ministry = Ministry.query.filter_by(ministry_id=ministry_id).first()

    if ministry is None:
        return redirect(url_for('create_ministry'))
    # TODO Add a form for selecting the date and destination of the cars
    # TODO Probably need to add all of the destinations available to the user

    return render_template('ministry.html', ministry=ministry, ride_form=ride_form, driver_form=driver_form)


@app.route('/driver/<ministry_id>')
def driver_signup(ministry_id):
    form = DriverSignupForm
    if form.validate_on_submit():
        driver_name = form.driver_name.data
        date = form.date.data
        dest = form.destination.data
        contact = form.contact.data
        open_seats = form.open_seats.data

        # TODO Take the form data and put it in the database
        return redirect(url_for('ministry'), ministry_id=ministry_id)

    return render_template('driver_signup.html', form=form)


@app.route('/ministry/<ministry_id>/<event_id>')
def event(ministry_id, event_id):
    ministry = Ministry.query.filter_by(ministry_id=ministry_id).first()

    if ministry is None:
        return redirect(url_for('create_ministry'))

    event = None
    # TODO parse the event to generate all of the cars that are available.

    # TODO display the cars in some sort of form.

    return render_template('car_select.html', ministry=ministry)
