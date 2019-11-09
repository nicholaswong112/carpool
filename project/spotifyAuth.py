import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.oauth2 as oauth2
from project.lookup import cred
from flask import redirect

#returns a sp_oauth object necessary for logging a user into spotify for the first time
#TODO can add a path that allows the redirect to go directly back to previous page

#def get_sp_oauth():
    
    #Need to more access to user data? Add more scopes here!
 #   SCOPE = 'playlist-read-private user-library-read playlist-modify-public playlist-modify-private'
  #  CACHE = '.spotipyoauthcache'
   # SPOTIPY_REDIRECT_URI = 'www.google.com'
    
    #TODO determine where to redirect after authorization by putting URI in SPOTIPY_REDIRECT_URI
    #sp_oauth2 = oauth2.SpotifyOAuth(cred.client_id, cred.client_secret,SPOTIPY_REDIRECT_URI,scope=SCOPE,cache_path=CACHE)
    #return sp_oauth2

#must be redirected to the URL link to login
    
#def get_url_for_user_login():
    
#    a_oauth_url = get_auth_object().get_authorize_url()
 #   return a_oauth_url

#use if just logged into spotify
#returns an array with access token first and refresh token second
#def extract_tokens_from_url(_the_sp_return_url):
    
#    sp_info = a_sp_oauth.get_access_token(get_auth_object, _the_sp_return_url)
#    return [sp_info.access_token, sp_info.refresh_token]
#might consider storing sp_info in db

def get_auth_object():
    #Need to more access to user data? Add more scopes here!
    SCOPE = 'playlist-read-private user-library-read playlist-modify-public playlist-modify-private'
    CACHE = '.spotipyoauthcache'
    SPOTIPY_REDIRECT_URI = "http://127.0.0.1:5000/auth/"
    #TODO determine where to redirect after authorization by putting URI in SPOTIPY_REDIRECT_URI
    sp_oauth = oauth2.SpotifyOAuth(cred.client_id, cred.client_secret,SPOTIPY_REDIRECT_URI,scope=SCOPE,cache_path=CACHE)

    return sp_oauth

def refresh_access_token(refresh_token):
    sp_oauth = get_auth_object()
    token_info = sp_oauth.refresh_access_token(refresh_token)
    return token_info['access_token']
