
from constants import SPOTIFY_TOKEN, SPOTIFY_USER_ID


class SpotifyClient(object):
    def __init__(self):
        self.spotify_token = SPOTIFY_TOKEN
        self.spotify_user_id = SPOTIFY_USER_ID

    def __str__(self):
        pass
