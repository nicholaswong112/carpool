from project import db

class Ministry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    password_hash = db.Column(db.String(128))
    rides = db.relationship('Ride', backref='ministry', lazy=True)

    def __repr__(self):
        return '<Ministry> {}'.format(self.name)

class Ride(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ministry_id = db.Column(db.Integer, db.ForeignKey('ministry.id'))
    dest = db.Column(db.String(64), index=True)
    date = db.Column(db.DateTime, index=True)
    time = db.Column(db.String(16))
    driver_name = db.Column(db.String(32))
    driver_addr = db.Column(db.String(64))
    driver_phone = db.Column(db.String(16))
    open_seats = db.Column(db.Integer)
    passengers = db.relationship('Passenger', backref='ride', lazy=True)

    def __repr__(self):
        return '<Ride> {} {} {} {}'.format(self.ministry_id, self.dest, self.date, self.driver_name)

class Passenger(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    addr = db.Column(db.String(64))
    phone = db.Column(db.String(16))
    ride_id = db.Column(db.Integer, db.ForeignKey('ride.id'))

    def __repr__(self):
        return '<Passenger> {}'.format(self.name)
