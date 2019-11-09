from project import socketio, db, spotify
from flask import session
from flask_socketio import send, emit, join_room, leave_room
from project.lookup import lookup
from project.models import User, Room, List, Song
from project.voting import generate_random_survey
from project.spotifyAuth import refresh_access_token
import threading

@socketio.on('join')
def updated_playlist(data):
    room_id = data['room_id']
    username = data['username']
    room = Room.query.filter_by(room_id=room_id).first()

    if room:
        join_room(room_id)
        user = User.query.filter_by(username=username).first()
        room.add_current_user(user)
        
        if not user.access_token:
            emit('prompt-auth-spotify')
        else:
            access_token = refresh_access_token(user.refresh_token)
            user.set_access_token(access_token)
            emit('close-auth-spotify')
        db.session.commit()
        emit('update-room-users', room.list_current_users(), room=room_id)

        suggested_songs = List.query.filter_by(list_id=room.suggest_list_id).first().list_songs()
        if suggested_songs:
            emit('update-sug-list', suggested_songs)

        playlist_id = room.playlist_id
        if playlist_id:
            emit('playlist-generation', 'spotify:playlist:' + playlist_id, room=room_id)

@socketio.on('leave')
def on_leave(data):
    room_id = data['room_id']
    username = data['username']
    room = Room.query.filter_by(room_id=room_id).first()

    if room:
        leave_room(room_id)
        user = User.query.filter_by(username=username).first()
        room.remove_current_user(user)
        db.session.commit()
        emit('update-room-users', room.list_current_users(), room=room_id)

@socketio.on('song-query')
def handle_song_query(data):
    query = str(data['query'])
    num_selections = int(data['num_selections'])
    suggestions = lookup.suggested_list(query, num_selections)
    emit('song-query-results', [vars(suggestion) for suggestion in suggestions])

@socketio.on('song-selection')
def handle_song_selection(selection_data):
    spotify_url = selection_data['spotify_url']
    room_id = selection_data['room_id']
    room = Room.query.filter_by(room_id=room_id).first()
    if room:
        chosen = lookup.get_track(spotify_url)
        db_song = Song.query.filter_by(spotify_url=spotify_url).first()
        if not db_song:
            db_song = Song(name=chosen.name, artist=chosen.main_artist(), album_cover=chosen.album_cover, spotify_url=chosen.spotify_url, uri=chosen.uri)
            db.session.add(db_song)

        suggestions = List.query.filter_by(list_id=room.suggest_list_id).first()
        if not suggestions.add_song(db_song):
            emit('result-message', "The song has already been added to the playlist.")
        else:
            db.session.commit()
            suggested_songs = suggestions.list_songs()
            emit('update-sug-list', suggested_songs, room=room_id)
    else:
        emit('result-message', "Sorry, the song was not added. Please try again.")

@socketio.on('begin-voting')
def handle_begin_voting(room_id):
    room = Room.query.filter_by(room_id=room_id).first()
    if room:
        suggestions = List.query.filter_by(list_id=room.suggest_list_id).first()
        suggestions.reset_votes()
        db.session.commit()
        suggested_songs = suggestions.list_songs()
        survey_list = generate_random_survey(suggested_songs)
        #send list somewhere else and get back
        emit('display-vote-songs', survey_list, room=room_id)

@socketio.on('finish-voting')
def handle_finish_voting(data):
    room_id = data['room_id']
    username = data['username']
    votes = data['votes']
    
    room = Room.query.filter_by(room_id=room_id).first()
    if room:
        suggestions = List.query.filter_by(list_id=room.suggest_list_id).first()
        for key in votes:
            num_vote = votes[key]
            vote = suggestions.vote_song(spotify_url=key, votes=num_vote)
            db.session.commit()

@socketio.on('collect-votes')
def handle_collect_votes(room_id):
    emit('submit-votes', room=room_id)

@socketio.on('end-voting')
def handle_end_voting(data):
    room_id = data['room_id']
    username = data['username']
    room = Room.query.filter_by(room_id=room_id).first()
    user = User.query.filter_by(username=username).first()
    
    if room:
        playlist_id = room.playlist_id

        suggestions = [song[0] for song in sorted(List.query.filter_by(list_id=room.suggest_list_id).first().list_votes(), key=lambda x: x[1], reverse=True)]
        vote_display = []
        
        if not playlist_id:
            playlist = spotify.create_playlist(room_id, user.access_token)
            playlist_id = playlist['id']
            room.playlist_id = playlist_id
            db.session.commit()
       
        #TODO add a check for whether user has authenticated and if not then don't end the voting process and instead prompt the user to log in.
        spotify.reset_and_add_to_playlist(playlist_id, suggestions, user.access_token)
        emit('playlist-generation', 'spotify:playlist:' + playlist_id, room=room_id)

        #for vote in suggestions_votes:
            #song = lookup.get_track(vote[0])
            #vote_display.append(song.name + " " + song.main_artist() + "\t" + str(vote[1]))
        #emit('display-votes', vote_display, room=room_id)

@socketio.on('chat-message')
def handle_chat_message(data, namespace='/chat'):
    msg = data['msg']
    room_id = data['room_id']
    username = data['username']
    emit('chat-message', username + ': ' + msg, room=room_id)
