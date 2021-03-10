
import emoji
import google_auth_oauthlib.flow
import googleapiclient.discovery
import os
import youtube_dl

from constants import CLIENT_SECRETS_FILE, SCOPES
from playlist import Playlist
from track import Track
from youtube_title_parse import get_artist_title


class YouTubeClient(object):
    def __init__(self):
        self.youtube_client = self.get_youtube_client()

    def __str__(self):
        return super().__str__()

    def get_youtube_client(self):
        # disable oauthlib's https verification when running locally
        # do not leave this option enabled in production, set os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = "0"
        os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = "1"

        api_service_name = "youtube"
        api_version = "v3"

        # get youtube credentials and create an api client from the youtube data api
        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
            CLIENT_SECRETS_FILE,
            SCOPES)

        # an authorization code will be asked for here
        credentials = flow.run_console()

        # youtube_client is a "googleapiclient.discovery.Resource" object
        youtube_client = googleapiclient.discovery.build(
            api_service_name,
            api_version,
            credentials=credentials)

        return youtube_client

    def get_youtube_playlists(self):
        request = self.youtube_client.playlists().list(
            part="id,snippet",
            maxResults=20,
            mine=True)

        response = request.execute()

        youtube_playlists = []
        for item in response['items']:
            youtube_playlists.append(
                Playlist(item['id'], item['snippet']['title']))

        # alternative implementation
        # youtube_playlists = [Playlist(item['id'], item['snippet']['title']) for item in response['items']]

        return youtube_playlists

    def get_videos_from_youtube_playlist(self, playlist_id):
        request = self.youtube_client.playlistItems().list(
            playlistId=playlist_id,
            part="id,snippet",
            maxResults=20)

        response = request.execute()

        tracks = []
        for item in response['items']:
            video_id = item['snippet']['resourceId']['videoId']

            artist, track_name = self.get_artist_and_track_from_youtube_video(
                video_id)

            if artist and track_name:
                tracks.append(Track(artist, track_name, video_id))

        return tracks

    def get_artist_and_track_from_youtube_video(self, video_id):
        youtube_url = f"https://www.youtube.com/watch?v={video_id}"

        video = youtube_dl.YoutubeDL({'quiet': True}).extract_info(
            youtube_url,
            download=False)

        try:
            artist, track = get_artist_title(video['title'])
        except TypeError as error_msg:
            # print(error_msg)

            # TEST on multiple video title scenarios
            artist = input(
                f"unrecognized artist\nplease provide the artist of the track \"{video['title']}\": ")
            track = video['title']

        # TODO handle artist and track formatting here

        # removes any emojis from the artist and track names
        artist = emoji.get_emoji_regexp().sub(u"", artist.lower().title())
        track = emoji.get_emoji_regexp().sub(u"", track.lower().title())

        # RESEARCH how to handle when artist/track naming format is swapped

        return artist, track

    # TEST experimental functionality
    """def get_liked_youtube_videos(self):
        # collect all liked videos and create a dictionary of track info
        request = self.youtube_client.videos().list(
            part="snippet,contentDetails,statistics",
            myRating="like"
        )

        response = request.execute()

        # collect each video and get important information
        for item in response['items']:
            video_title = item['snippet']['title']
            youtube_url = f"https://www.youtube.com/watch?v={item['id']}"

            # use youtube_dl to collect the artist and track name
            video = youtube_dl.YoutubeDL({}).extract_info(
                youtube_url, download=False)

            artist = video['artist']
            track_name = video['track']

            if artist is not None and track_name is not None:
                spotify_client = SpotifyClient()

                spotify_uri = spotify_client.search_spotify_track(
                    artist,
                    track_name)

                # adjust function if changes happen to track info ?
                # spotify_uri, track_id = self.search_spotify_track(artist, track_name)

                # collect all relevant track info and skip any missing tracks and artists
                self.track_info[video_title] = {
                    "youtube_url": youtube_url,
                    "spotify_uri": spotify_uri,
                    "artist": artist,
                    "track_name": track_name,
                    # "track_id": track_id
                }
    """
