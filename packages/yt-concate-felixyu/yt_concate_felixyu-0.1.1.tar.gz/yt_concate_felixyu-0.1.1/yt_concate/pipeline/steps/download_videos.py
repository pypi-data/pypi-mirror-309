import yt_dlp
import time
import logging
import concurrent.futures
from .step import Step


class DownloadVideos(Step):
    def process(self, data, inputs, utils):
        logger = logging.getLogger()
        yt_set = set([found.yt for found in data])
        fast = inputs['fast']
        start = time.time()

        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            future = {executor.submit(self.downloadvideo, yt, utils, fast): yt for yt in yt_set}

        end = time.time()
        logger.info('==> Download videos took ', end - start, ' seconds.')
        #Utils.convert_video_to_mp4()

        return data

    @staticmethod
    def downloadvideo(yt, utils, fast):
        logger = logging.getLogger()
        # 設定 yt-dlp 的下載選項
        ydl_opts = {
            'format': 'bestvideo+bestaudio/best',  # 下載最好的可用影片質量
            # 'merge_output_format': 'mp4',
            'outtmpl': yt.video_filepath,  # 自定義輸出檔案名稱，影片標題加上副檔名
            'nooverwrites': True,
        }
        # ydl_opts['outtmpl'] = yt.video_filepath

        logger.info('Downloading video for ', yt.url)
        if fast == 'True':
            if utils.video_file_exists(yt):
                logger.debug('found existing video file')
                return

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download(yt.url)
        return