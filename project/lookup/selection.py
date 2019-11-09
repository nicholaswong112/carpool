# Holds relevant information of a song
class Selection:
    def __init__(self, name, artists, explicit, spotify_url, uri, preview_url, album_cover):
        self.name = name
        self.artists = artists
        self.explicit = explicit
        self.spotify_url = spotify_url
        self.uri = uri
        self.preview_url = preview_url
        self.album_cover = album_cover

    def main_artist(self):
        return self.artists[0]
