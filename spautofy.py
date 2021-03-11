
from constants import DEBUG_MODE
from spotify_client import SpotifyClient
from youtube_client import YouTubeClient
from youtube_playlist import YouTubePlaylist
from youtube_video import YouTubeVideo


class Spautofy(object):
    def __init__(self):
        self.run()

    def __str__(self):
        return super().__str__()

    def run(self):
        youtube_client = YouTubeClient()

        youtube_playlists = youtube_client.get_user_playlists()

        while True:
            # prompt a user to choose from a list of their existing youtube playlists
            for i, playlist in enumerate(youtube_playlists):
                print(f"{i}: {playlist.playlist_name}")

            try:
                selected_playlist = int(
                    input("select a playlist to export tracks from: "))
                break
            except ValueError:
                if DEBUG_MODE:
                    print("input not recognized, please try again ...\n")
                    continue

        selected_playlist = youtube_playlists[selected_playlist]

        youtube_videos = youtube_client.get_playlist_videos(
            selected_playlist.playlist_id)

        if not youtube_videos:
            if DEBUG_MODE:
                print("the youtube playlist is empty\n")
        else:
            spotify_client = SpotifyClient()

            for track in youtube_videos:
                if DEBUG_MODE:
                    print(
                        f"\nartist: {track.artist}\ntrack: {track.track_name}")

                spotify_track_id = spotify_client.search_track(
                    track.artist, track.track_name)

                spotify_track_id_found = bool(spotify_track_id)

                if spotify_track_id_found:
                    spotify_client.add_track_to_liked_songs(spotify_track_id)
