
import emoji
import google_auth_oauthlib.flow
import googleapiclient.discovery
import os
import youtube_dl

from constants import CLIENT_SECRETS_FILE, SCOPES
from youtube_playlist import YouTubePlaylist
from youtube_title_parse import get_artist_title
from youtube_video import YouTubeVideo


class YouTubeClient(object):
    # RESEARCH django functionality - using spotify 2fa as a login method to pull a users account
    # details (playlists, liked songs, etc.) to use the program for their own account

    def __init__(self):
        self.youtube_client = self.get_client()

    def __str__(self):
        return super().__str__()

    def get_client(self):
        # disable oauthlib's https verification when running locally
        # do not leave this option enabled in production, set os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = "0"
        os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = "1"
        api_service_name = "youtube"
        api_version = "v3"

        # get youtube credentials and create an api client from the youtube data api
        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
            CLIENT_SECRETS_FILE, SCOPES)

        # an authorization code will be asked for here
        credentials = flow.run_console()

        # youtube_client is a "googleapiclient.discovery.Resource" object
        youtube_client = googleapiclient.discovery.build(
            api_service_name, api_version, credentials=credentials)

        return youtube_client

    def get_user_playlists(self):
        # https://developers.google.com/youtube/v3/docs/playlists/list
        request = self.youtube_client.playlists().list(part="id,snippet", mine=True)

        response = request.execute()

        # TODO write out response info to a file (formatted)
        # TODO extract additional playlist attrs (refer spotify_client.py)
        playlist_info = response['items']
        playlists = []

        for attr in playlist_info:
            playlists.append(YouTubePlaylist(
                attr['id'], attr['snippet']['title']))

        # alternative implementation
        # playlists = [YouTubePlaylist(attr['id'], attr['snippet']['title']) for attr in playlist_info]

        return playlists

    def get_playlist_videos(self, playlist_id):
        # https://developers.google.com/youtube/v3/docs/playlistItems/list
        request = self.youtube_client.playlistItems().list(
            part="id,snippet", playlistId=playlist_id)

        response = request.execute()

        # TODO write out response info to a file (formatted)
        # TODO extract additional video attrs (refer spotify_client.py)
        video_info = response['items']
        videos = []

        for attr in video_info:
            video_id = attr['snippet']['resourceId']['videoId']

            artist, track_name = self.get_playlist_video_track_info(video_id)

            if artist and track_name:
                videos.append(YouTubeVideo(artist, track_name))

        return videos, video_id

    def get_playlist_video_track_info(self, video_id):
        url = f"https://www.youtube.com/watch?v={video_id}"

        video = youtube_dl.YoutubeDL(
            {'quiet': True}).extract_info(url, download=False)

        try:
            artist, track_name = get_artist_title(video['title'])
        except TypeError:
            artist = input(
                f"unrecognized artist\nplease provide the artist of the track \"{video['title']}\": ")
            track_name = video['title']

        # removes any emojis from the artist and track names
        # TODO remove extra whitespaces
        artist = emoji.get_emoji_regexp().sub(u"", artist.lower().title())
        track_name = emoji.get_emoji_regexp().sub(u"", track_name.lower().title())

        # TODO youtube/spotify overlap to begin here
        # TODO youtube video title cross validation with spotify track
        # RESEARCH how to handle when artist/track youtube video naming format is swapped
        return artist, track_name

    # TEST
    """self.track_info = {}
    def get_liked_videos(self):
        # https://developers.google.com/youtube/v3/docs/videos/list
        request = self.youtube_client.videos().list(
            part="snippet,contentDetails,statistics", myRating="like")

        response = request.execute()

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
                    artist, track_name)

                # adjust function if changes happen to track info ?
                # spotify_uri, track_id = self.search_spotify_track(artist, track_name)

                # collect all relevant track info and skip any missing tracks and artists
                self.track_info[video_title] = {
                    "youtube_url": youtube_url,
                    "spotify_uri": spotify_uri,
                    "artist": artist,
                    "track_name": track_name,
                    # "track_id": track_id
                }"""
