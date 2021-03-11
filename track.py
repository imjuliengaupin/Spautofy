
class Track(object):
    def __init__(self, artist, track_name, youtube_video_id):
        self.artist = artist
        self.track_name = track_name
        self.youtube_video_id = youtube_video_id

    def __str__(self):
        return f"artist: {self.artist}\ntrack: {self.track_name}\nvideo id: {self.youtube_video_id}"
