import logging

import yt_dlp
import time
import concurrent.futures
from .step import Step


class DownloadCaptions(Step):
    def process(self, data, inputs, utils):
        logger = logging.getLogger()
        fast = inputs['fast']
        start = time.time()

        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            future = {executor.submit(self.downloadcaption, yt, utils, fast): yt for yt in data}

        end = time.time()
        logger.info('==> Download captions took ', end-start, ' seconds.')
        return data

    @staticmethod
    def downloadcaption(yt, utils, fast):
        logger = logging.getLogger()
        logger.info('Downloading caption for ', yt.id)

        if fast == 'True':
            if utils.caption_file_exists(yt):
                logger.debug('found existing caption file')
                return

        try:
            ydl_opts = {
                'writesubtitles': True,  # 下載字幕
                'writeautomaticsub': True,
                'subtitleslangs': ['en'],
                'subtitlesformat': 'vtt',
                'skip_download': True,
                'outtmpl': yt.caption_filepath,
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download(yt.url)

            utils.convert_vtt_to_srt(yt)
        except (KeyError, AttributeError):
            logger.debug('Error when downloading caption for ', yt.url)
            return

        return

