from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
from project.lookup import selection, cred


def suggested_list(input_str, num_args):
    
    client_credentials_manager = SpotifyClientCredentials(client_id=cred.client_id,
                                                          client_secret=cred.client_secret)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    results = sp.search(q=input_str, limit=num_args)

    suggestions = []

    for i, t in enumerate(results['tracks']['items']):
        
        artists = []
        for j in t['artists']:
            artists.append(j['name'])

        temp = selection.Selection(name=t['name'], artists=artists, explicit=t['explicit'],
                                   spotify_url=t['external_urls']['spotify'], uri=t['uri'],
                                   preview_url=t['preview_url'], album_cover=t['album']['images'][0]['url'])
        suggestions.append(temp)

    return suggestions

def get_track(input_str):

    client_credentials_manager = SpotifyClientCredentials(client_id=cred.client_id,
                                                          client_secret=cred.client_secret)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    result = sp.track(track_id=input_str)

    artists = []
    for i in result['artists']:
        artists.append(i['name'])
    temp = selection.Selection(name=result['name'], artists=artists, explicit=result['explicit'],
                                   spotify_url=result['external_urls']['spotify'], uri=result['uri'],
                                   preview_url=result['preview_url'], album_cover=result['album']['images'][0]['url'])
    
    return temp
