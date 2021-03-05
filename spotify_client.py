
# generate new spotify tokens at https://developer.spotify.com/console
# spotify tokens expire every 1 hour
SPOTIFY_TOKEN = ""
SPOTIFY_USER_ID = ""


class SpotifyClient(object):
    def __init__(self):
        self.spotify_token = SPOTIFY_TOKEN
        self.spotify_user_id = SPOTIFY_USER_ID

    def __str__(self):
        pass
