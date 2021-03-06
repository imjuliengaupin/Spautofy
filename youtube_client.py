
CLIENT_SECRETS_FILE = "./credentials/client_secret.json"
SCOPES = ['https://www.googleapis.com/auth/youtube.readonly']


class YouTubeClient(object):
    def __init__(self):
        self.youtube_client = self.get_youtube_client()

    def __str__(self):
        return str(self.youtube_client)

    def get_youtube_client(self):
        import google_auth_oauthlib.flow
        import googleapiclient.discovery
        import os

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

        # NOTE youtube_client is a "googleapiclient.discovery.Resource" object
        youtube_client = googleapiclient.discovery.build(
            api_service_name,
            api_version,
            credentials=credentials)

        return youtube_client
