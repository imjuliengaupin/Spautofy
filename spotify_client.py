
import requests

from constants import SPOTIFY_TOKEN, SPOTIFY_USER_ID


class SpotifyClient(object):
    def __init__(self):
        self.oauth_token = SPOTIFY_TOKEN
        self.user_id = SPOTIFY_USER_ID

    def __str__(self):
        return f"oauth token: {self.oauth_token}\nuser id: {self.user_id}"

    def get_track_id(self, track_info):
        return track_info[0]['id']

    def get_track_name(self, track_info):
        return track_info[0]['name']

    def get_artist(self, track_info):
        artist_info = track_info[0][['artists'][0]]
        return artist_info[0]['name']

    def get_album(self, track_info):
        album_info = track_info[0][['album'][0]]
        return album_info['name']

    def search_track(self, artist, track_name):
        search_query = f"https://api.spotify.com/v1/search?query=track%3A{track_name}+artist%3A{artist}&type=track&offset=0&limit=20"

        response = requests.get(
            search_query,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.oauth_token}"})

        json_response = response.json()

        try:
            track_info = json_response['tracks']['items']
        except KeyError:
            print(
                f"{self.oauth_token} has expired\nplease renew your Spotify token ...")

        track_found = bool(track_info)

        if(track_found):
            return self.get_track_id(track_info)
        else:
            # FIXME implement a better way to handle this function return
            return None

    def add_track_to_liked_songs(self, track_id):
        url = "https://api.spotify.com/v1/me/tracks"

        response = requests.put(
            url,
            json={
                "ids": [track_id]},
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.oauth_token}"})

        # FIXME implement a better way to handle this function return
        return response.ok

    # TEST
    """def create_a_playlist(self):
        request = json.dumps({
            "name": "Spautofy",
            "description": "",
            "public": False  # creates a private playlist
        })

        query = f"https://api.spotify.com/v1/users/{self.user_id}/playlists"

        response = requests.post(
            query,
            data=request,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.oauth_token}"})

        playlist = response.json()

        return playlist['id']

    def add_track_to_spotify_playlist(self):
        youtube_client = YouTubeClient()

        playlist_id = self.create_a_playlist()

        # add all liked tracks from youtube into the new spotify playlist
        # and populate a dictionary with the tracks info
        youtube_client.get_liked_youtube_videos()

        uris = []

        for track, info in self.track_info.items():
            uris.append(info['spotify_uri'])

        # alternative implementation
        # uris = [info['spotify_uri'] for track, info in self.track_info.items()]

        # add all tracks into the new playlist
        request = json.dumps(uris)

        query = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"

        response = requests.post(
            query,
            data=request,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.oauth_token}"})

        # check for a valid response status
        if response.status_code != 200:
            raise Exception(response.status_code)

        json_response = response.json()

        return json_response"""
