from flask import render_template, flash, redirect, url_for, request
from project import app, db
from project.forms import CreateministryForm, FindministryForm, RideSearchForm, DriverSubmitForm, DriverSignupForm, \
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
            return redirect(url_for('find_ministry'))
        else:
            return redirect(url_for('ministry', ministry_id=form.ministry_id.data))

    return render_template('find-ministry.html', title='Find Your Ministry', form=form)


@app.route('/createministry', methods=['GET', 'POST'])
def create_ministry():
    form = CreateministryForm()

    if form.validate_on_submit():
        ministry_id = generate_rand_ministry_id()  # TODO look at this after db ready

        while Ministry.query.filter_by(ministry_id=ministry_id).first() is not None:
            ministry_id = generate_rand_ministry_id()

        new_ministry = Ministry(ministry_id=ministry_id, ministry_name=form.ministry_name.data)
        db.session.add(new_ministry)
        db.session.commit()

        flash('Your ministry code is ' + ministry_id)
        return redirect(url_for('ministry', ministry_id=ministry_id))
    else:
        form.ministry_name.data = "Ministry"

    return render_template('create-ministry.html', title='Create ministry', form=form)


def generate_rand_ministry_id():
    return ''.join([random.choice(string.ascii_lowercase) for _ in range(5)])


@app.route('/ministry/<ministry_id>', methods=['GET', 'POST'])
def ministry(ministry_id):
    ride_form = RideSearchForm()
    if ride_form.validate_on_submit():
        date = ride_form.date.data
        date_str = convert_datetime_to_str(date)
        return redirect(url_for('ministry'), ministry_id=ministry_id, date_str=date_str)

    driver_form = DriverSubmitForm()
    if driver_form.validate_on_submit():
        return redirect(url_for('driver'), ministry_id=ministry_id)

    ministry = Ministry.query.filter_by(ministry_id=ministry_id).first()

    if ministry is None:
        return redirect(url_for('create_ministry'))

    return render_template('ministry.html', ministry=ministry, ride_form=ride_form, driver_form=driver_form)


@app.route('/driver/<ministry_id>', methods=['GET', 'POST'])
def driver_signup(ministry_id):
    form = DriverSignupForm
    if form.validate_on_submit():
        driver_name = form.driver_name.data
        driver_addr = form.driver_addr.data
        driver_phone= form.driver_phone.data
        date = form.date.data
        time = form.time.data
        dest = form.destination.data
        open_seats = form.open_seats.data
        new_ride = Ride(ministry_id=ministry_id, driver_name=driver_name, driver_addr=driver_addr,
                        driver_phone=driver_phone, date=date, time=time, dest=dest, open_seats=open_seats)
        db.session.add(new_ride)
        db.session.commit()

        return redirect(url_for('ministry'), ministry_id=ministry_id)

    return render_template('driver-signup.html', form=form)


def convert_str_to_datetime(date_str):
    return DateTime.parse(date_str[0:2] + '//' + date_str[2:4] + '//' + date_str[4:8])


def convert_datetime_to_str(date):
    month = date.strftime('%m')
    day = date.strftime('%d')
    year = date.strftime('%Y')
    return str(month) + str(day) + str(year)


@app.route('/ministry/<ministry_id>/<date_str>', methods=['GET', 'POST'])
def show_rides(ministry_id, date_str):
    ministry = Ministry.query.filter_by(ministry_id=ministry_id).first()

    if ministry is None:
        return redirect(url_for('create_ministry'))

    datetime = convert_str_to_datetime(date_str)

    # TODO see if this filtering works or if there is some other way that we should filter for rides in the ministry
    #  group on this day
    rides = ministry.rides.query.filter_by(date=datetime)

    ride_dict = dict()
    open_rides = []
    closed_rides = []

    for ride in rides:
        if ride.open_seats > 0:
            driver_name = ride.driver_name
            dest = ride.dest
            time = ride.time
            open_seats = ride.open_seats
            driver_details = 'Name: ' + driver_name + ' Destination: ' + dest + ' Time: ' + time + ' Open Seats: ' + \
                             open_seats
            open_rides.append(driver_details)
            ride_dict[driver_details] = ride.id
        else:
            closed_rides.append('Name: ' + driver_name + ' Destination: ' + dest + ' Time: ' + time + ' Open Seats: ')

    form = RideDisplayForm()
    form.driver_details.choices = open_rides
    if form.validate_on_submit():
        selected_driver = form.ride_details.data
        ride_id = ride_dict[selected_driver]
        redirect(url_for('passenger_signup'), ministry_id=ministry_id, ride_id=ride_id)

    return render_template('ride-select.html', ministry=ministry, form=form, closed_rides=closed_rides)


@app.route('/passenger_signup/<ministry_id>/<ride_id>', methods=['GET', 'POST'])
def passenger_signup(ministry_id, ride_id):
    ride = Ride.query.filter_by(id=ride_id).first()

    if ride is None or ride.open_seats < 1:
        flash('Ride is invalid. Please try to find a different ride.')
        redirect(url_for('ministry'), ministry_id)

    form = PassengerSignupForm()
    if form.validate_on_submit():
        if ride.open_seats < 1:
            flash('Ride is invalid. Please try to find a different ride.')
            redirect(url_for('ministry'), ministry_id)
        passenger_name = form.passenger_name.data
        passenger_phone = form.passenger_phone.data
        passenger_addr = form.passenger_addr.data
        new_passenger = Passenger(name=passenger_name, phone=passenger_phone, addr=passenger_addr, ride_id=ride_id)
        db.session.add(new_passenger)
        db.session.commit()
        redirect(url_for('ministry'), ministry_id)

    return render_template('passenger-signup.html', ministry_id=ministry_id, ride_id=ride_id, form=form)

