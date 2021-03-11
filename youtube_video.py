
class YouTubeVideo(object):
    def __init__(self, artist, track_name):
        self.artist = artist
        self.track_name = track_name

    def __str__(self):
        return f"artist: {self.artist}\ntrack: {self.track_name}"
