
from constants import DEBUG_MODE
from spotify_client import SpotifyClient
from youtube_client import YouTubeClient


class Spautofy(object):
    def __init__(self):
        self.run()

    def __str__(self):
        return super().__str__()

    def run(self):
        youtube_client = YouTubeClient()
        youtube_playlists = youtube_client.get_youtube_playlists()

        # prompt a user to choose from a list of their existing youtube playlists
        for index, playlist in enumerate(youtube_playlists):
            print(f"{index}: {playlist.playlist_title}")

        selected_playlist = int(
            input("select a youtube playlist to export tracks from: "))

        # for each video in the selected youtube playlist, collect the track information
        selected_playlist = youtube_playlists[selected_playlist]

        youtube_videos = youtube_client.get_videos_from_youtube_playlist(
            selected_playlist.playlist_id)

        spotify_client = SpotifyClient()

        if not youtube_videos:
            if DEBUG_MODE:
                print("the youtube playlist is empty")
        else:
            for track in youtube_videos:
                if DEBUG_MODE:
                    print(
                        f"artist: {track.artist}\ntrack: {track.track_name}\nyoutube video id: {track.youtube_video_id}")

                spotify_track_id = spotify_client.search_spotify_track(
                    track.artist, track.track_name)

                spotify_track_id_found = bool(spotify_track_id)

                if spotify_track_id_found:
                    if DEBUG_MODE:
                        print(f"spotify track id: {spotify_track_id}\n")
                else:
                    if DEBUG_MODE:
                        print(
                            f"spotify track id: \"{track.artist} - {track.track_name}\" was not found\n")
