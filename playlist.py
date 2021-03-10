
class Playlist(object):
    def __init__(self, playlist_id, playlist_title):
        self.playlist_id = playlist_id
        self.playlist_title = playlist_title

    def __str__(self):
        return f"id: {self.playlist_id}\nplaylist: {self.playlist_title}"
