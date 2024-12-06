from dotenv import load_dotenv
import os
import logging

load_dotenv()
API_KEY = os.getenv('API_KEY')

DOWNLOADS_DIR = 'downloads'
VIDEOS_DIR = os.path.join(DOWNLOADS_DIR, 'videos')
CAPTIONS_DIR = os.path.join(DOWNLOADS_DIR, 'captions')
OUTPUTS_DIR = 'outputs'
LOGS_DIR = 'logs'

CAPTION_FILE_EXT_EN_VTT = '.en.vtt'
CAPTION_FILE_EXT_EN_SRT = '.en.srt'

VIDEO_FILE_EXT = '.mp4'

FILE_LOGGING_LEVEL = logging.DEBUG