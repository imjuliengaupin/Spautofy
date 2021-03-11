
import requests

from constants import SPOTIFY_TOKEN, SPOTIFY_USER_ID


class SpotifyClient(object):
    def __init__(self):
        self.spotify_token = SPOTIFY_TOKEN
        self.spotify_user_id = SPOTIFY_USER_ID

    def __str__(self):
        return f"token: {self.spotify_token}\nuser_id: {self.spotify_user_id}"

    def search_spotify_track(self, artist, track_name):
        # TEST handle artist and track formatting here ?
        query = f"https://api.spotify.com/v1/search?query=track%3A{track_name}+artist%3A{artist}&type=track&offset=0&limit=20"

        response = requests.get(
            query,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.spotify_token}"
            }
        )

        json_response = response.json()

        try:
            track_info = json_response['tracks']['items']
            track_found = bool(json_response.get(
                'tracks', {}).get('items', []))
        except KeyError as error_msg:
            # print(error_msg)
            print(
                f"{self.spotify_token} has expired\nplease renew your Spotify token ...")

        if(track_found):
            # if required, additional details include [0]['uri'], [0]['name'], [0]['type'] ...
            track_id = track_info[0]['id']  # only use the first song
            return track_id
        else:
            return None
