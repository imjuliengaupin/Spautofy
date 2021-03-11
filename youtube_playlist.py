
class YouTubePlaylist(object):
    def __init__(self, playlist_id, playlist_name):
        self.playlist_id = playlist_id
        self.playlist_name = playlist_name

    def __str__(self):
        return f"playlist id: {self.playlist_id}\nplaylist: {self.playlist_name}"
