from project import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from hashlib import md5
from datetime import datetime


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    access_token = db.Column(db.String(300), default='')
    refresh_token = db.Column(db.String(300), default='')
    invisible = db.Column(db.Boolean, default=False)
   
    def __repr__(self):
        return '<User {}>'.format(self.username)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def set_access_token(self, token):
        self.access_token = token

    def set_refresh_token(self, token):
        self.refresh_token = token

auth_users = db.Table('auth_users', 
    db.Column('room_id', db.Integer, db.ForeignKey('room.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
)

room_users = db.Table('room_users',
    db.Column('room_id', db.Integer, db.ForeignKey('room.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
)

class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    room_name = db.Column(db.String(30), default="")
    room_id = db.Column(db.String(10), index=True, unique=True)
    suggest_list_id = db.Column(db.String(11))
    gen_list_id = db.Column(db.String(11))
    playlist_id = db.Column(db.String(30), default='')
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    password_required = db.Column(db.Boolean(), default=True)
    password_hash = db.Column(db.String(128))
    last_used = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    authorized = db.relationship('User', secondary=auth_users, lazy='dynamic')
    current_users = db.relationship('User', secondary=room_users, lazy='dynamic')

    def __repr__(self):
        return '<Room {}>'.format(self.room_id)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def add_user(self, user):
        if not self.check_user(user):
            self.authorized.append(user)
    
    def check_user(self, user):
        return self.authorized.filter(
            auth_users.c.user_id == user.id).count() > 0

    def add_current_user(self, user):
        if self.current_users.filter(room_users.c.user_id == user.id).count() == 0: #and not user.invisible:
            self.current_users.append(user)

    def remove_current_user(self, user):
        if self.current_users.filter(room_users.c.user_id == user.id).count() > 0:
            self.current_users.remove(user)

    def list_current_users(self):
        ret = []
        for user in self.current_users:
            ret.append(user.username)
        return ret

    def check_owner(self, user):
        return self.owner_id == user.id

    def set_suggest_list(self, list):
        self.suggest_list_id = self.room_id + '1'
        list.room_id = self.room_id
        list.list_id = self.suggest_list_id
        db.session.commit()

    def set_gen_list(self, list):
        self.gen_list_id = self.room_id + '2'
        list.room_id = self.room_id
        list.list_id = self.gen_list_id
        db.session.commit()

song_lists = db.Table('song_lists',
    db.Column('list_id', db.Integer, db.ForeignKey('list.id')),
    db.Column('song_id', db.Integer, db.ForeignKey('song.id'))
)

class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    artist = db.Column(db.String(100))
    album_cover = db.Column(db.String(200))
    uri = db.Column(db.String(200))
    spotify_url = db.Column(db.String(200))

    def __repr__(self):
        return '<Song {}>'.format(self.name)

# Might want to completely clean up and reformat database
class SongMeta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    spotify_url = db.Column(db.String(200))
    suggested_by = db.Column(db.String(64))
    last_played = db.Column(db.Integer(), default=0)
    num_votes = db.Column(db.Integer(), default=0)
    list_id = db.Column(db.Integer, db.ForeignKey('list.id'))

    def __repr__(self):
        return '<Song {}>'.format(self.spotify_url)

class List(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    list_id = db.Column(db.String(11))
    room = db.Column(db.Integer, db.ForeignKey('room.id'))
    songs = db.relationship('Song', secondary=song_lists, lazy='dynamic')
    song_metas = db.relationship('SongMeta', lazy='dynamic')

    def add_song(self, song):
        if not self.check_song(song):
            self.songs.append(song)
            self.song_metas.append(SongMeta(spotify_url=song.spotify_url, list_id=self.id))
            return True
        else:
            return False

    def check_song(self, song):
        return self.songs.filter(
            song_lists.c.song_id == song.id).count() > 0

    def vote_song(self, spotify_url, votes):
        meta = self.song_metas.filter_by(spotify_url=spotify_url).first()
        if meta is not None:
            meta.num_votes = meta.num_votes + votes
            return True
        else:
            return False

    def list_songs(self):
        #TODO naming
        ret = []
        for song in self.songs:
           ret.append([song.name, song.artist, song.album_cover, song.spotify_url])
        return ret

    def list_votes(self):
        ret = []
        for song in self.songs:
            meta = self.song_metas.filter_by(spotify_url=song.spotify_url).first()
            ret.append([song.spotify_url, meta.num_votes])
        return ret

    def reset_votes(self):
        for meta in self.song_metas:
            meta.num_votes = 0
    
    def __repr__(self):
        return '<List>' #TODO

@login.user_loader
def load_user(id):
    return User.query.get(int(id))
