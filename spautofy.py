
import getpass

from constants import DEBUG_MODE
from spotify_client import SpotifyClient
from youtube_client import YouTubeClient
from youtube_playlist import YouTubePlaylist
from youtube_to_mp3 import YouTubeToMp3
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
                selected_youtube_playlist = int(
                    input("select a playlist to export tracks from: "))
                break
            except ValueError:
                if DEBUG_MODE:
                    print("input not recognized, please try again ...\n")
                    continue

        selected_youtube_playlist = youtube_playlists[selected_youtube_playlist]

        youtube_videos, video_id = youtube_client.get_playlist_videos(
            selected_youtube_playlist.playlist_id)

        if not youtube_videos:
            if DEBUG_MODE:
                print("the youtube playlist is empty\n")
        else:
            spotify_client = SpotifyClient()

            for youtube_track in youtube_videos:
                if DEBUG_MODE:
                    print(
                        f"\nartist: {youtube_track.artist}\ntrack: {youtube_track.track_name}")

                spotify_track_id = spotify_client.search_track(
                    youtube_track.artist, youtube_track.track_name)

                spotify_track_id_found = bool(spotify_track_id)

                if spotify_track_id_found:
                    spotify_track_added = bool(
                        spotify_client.add_track_to_liked_songs(spotify_track_id))

                    if spotify_track_added:
                        print(
                            f"\"{youtube_track.artist} - {youtube_track.track_name}\" has been added to your spotify liked songs")
                    else:
                        pass
                else:
                    print(
                        f"\"{youtube_track.artist} - {youtube_track.track_name}\" was not found on spotify, downloading mp3 ...")

                    # TODO handle the scenario where if the file being converted already exists in the local files path
                    spotify_local_files_path = f"/Users/{getpass.getuser()}/Music/"
                    # BUG video_id referencing the last video in the selected youtube playlist every time
                    youtube_video_url = f"https://www.youtube.com/watch?v={video_id}"

                    # TEST are the youtube_track.artist and youtube_track.track_name string values free of emojis, special characters, etc. ?
                    file_name = f"{youtube_track.artist} - {youtube_track.track_name}"

                    YouTubeToMp3(youtube_video_url).download_audio(
                        spotify_local_files_path, file_name)

                    # TODO convert the downloaded mp4 to mp3 format
