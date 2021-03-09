
from constants import DEBUG_MODE
from youtube_client import YouTubeClient


class Spautofy(object):
    def __init__(self):
        self.run()

    def __str__(self):
        return super().__str__()

    def run(self):
        youtube_client = YouTubeClient()
        youtube_playlists = youtube_client.get_youtube_playlists()

        if DEBUG_MODE:
            # prompt a user to choose from a list of their existing youtube playlists
            for index, playlist in enumerate(youtube_playlists):
                print(f"{index}: {playlist.playlist_title}")

            selected_playlist = int(
                input("select a youtube playlist to export tracks from: "))

            # for each video in the selected youtube playlist, collect the track information
            selected_playlist = youtube_playlists[selected_playlist]
            print(selected_playlist)
        else:
            pass
