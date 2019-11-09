import spotipy
import spotipy.oauth2 as oauth2
from spotipy.oauth2 import SpotifyClientCredentials
from project.lookup import cred

def create_playlist(name, auth_token):
    sp = spotipy.Spotify(auth=auth_token)
    return sp.user_playlist_create(sp.current_user()['id'], name)

def add_to_playlist(playlist_id, songs, auth_token):
    sp = spotipy.Spotify(auth=auth_token)
    sp.user_playlist_add_tracks(sp.current_user()['id'], playlist_id, songs)

def reset_and_add_to_playlist(playlist_id, songs, auth_token):
    sp = spotipy.Spotify(auth=auth_token)
    sp.user_playlist_replace_tracks(sp.current_user()['id'], playlist_id, songs)
