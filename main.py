from project import app, db, socketio
from project.models import User, Song, Room, List
from project.__init__ import os

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Song': Song, 'Room': Room, 'List': List}

if __name__ == '__main__':
    app.debug=True
    #port=int(os.environ.get("PORT", 5000))
    socketio.run(app)
