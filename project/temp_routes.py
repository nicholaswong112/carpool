from flask import render_template, request, url_for, redirect
from project import app, db
from project.models import Ministry, Ride, Passenger
from datetime import datetime

@app.route('/')
def index():
    ministries = Ministry.query.all()
    rides = Ride.query.all()
    passengers = Passenger.query.all()
    return render_template('index.html', ministries=ministries, rides=rides, passengers=passengers)

@app.route('/ministry', methods=['POST'])
def ministry():
    if request.form:
        ministry = Ministry(name=request.form['name'], password_hash='000')
        db.session.add(ministry)
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/ride', methods=['POST'])
def ride():
    if request.form:
        ride = Ride(ministry_id=request.form['ministry_id'], dest=request.form['dest'], date=datetime.strptime(request.form['date'], '%m/%d/%y'), driver_name=request.form['driver_name'])
        db.session.add(ride)
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/passenger', methods=['POST'])
def passenger():
    if request.form:
        passenger = Passenger(name=request.form['name'], addr='ADDR', phone='000', ride_id=1)
        db.session.add(passenger)
        db.session.commit()
    return redirect(url_for('index'))