from project import app, db
from project.models import Ministry, Ride
from project.__init__ import os

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Ministry': Ministry, 'Ride': Ride}

if __name__ == '__main__':
    app.debug=True
    app.run()
