
class Track(object):
    def __init__(self, artist, track_name, video_id):
        self.artist = artist
        self.track_name = track_name
        self.video_id = video_id

    def __str__(self):
        return f"artist: {self.artist}\ntrack: {self.track_name}\nvideo id: {self.video_id}"
