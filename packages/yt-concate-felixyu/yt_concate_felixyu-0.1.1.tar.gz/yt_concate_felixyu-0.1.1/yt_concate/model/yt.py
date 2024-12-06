import os

from yt_concate.settings import CAPTIONS_DIR
from yt_concate.settings import VIDEOS_DIR


class YT:
    def __init__(self, url):
        self.url = url
        self.id = self.get_video_id_from_url(url)
        self.caption_filepath = self.get_caption_path()
        self.video_filepath = self.get_video_path()
        self.captions = None

    def __str__(self):
        return '<YT('+self.id+')>'

    def __repr__(self):
        content = ' : '.join([
            '\nid='+str(self.id),
            '\ncaption_filepath='+str(self.caption_filepath),
            '\nvideo_filepath='+str(self.video_filepath)
        ])
        return '<YT('+content+')>'

    @staticmethod
    def get_video_id_from_url(url):
        return url.split('watch?v=')[-1]

    def get_caption_path(self):
        return os.path.join(CAPTIONS_DIR, self.id)

    def get_video_path(self):
        return os.path.join(VIDEOS_DIR, self.id)