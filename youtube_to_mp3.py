
from pytube import YouTube
from pytube.exceptions import RegexMatchError


class YouTubeToMp3(object):
    def __init__(self, video_url):
        self.video_url = video_url

    def download_audio(self, output_path, file_name):
        try:
            pytube = YouTube(self.video_url)
            youtube_video = pytube.streams.filter(
                only_audio=True).asc().first()
            youtube_video.download(output_path, file_name)
        except RegexMatchError as error:
            # url was not provided
            print(error)
