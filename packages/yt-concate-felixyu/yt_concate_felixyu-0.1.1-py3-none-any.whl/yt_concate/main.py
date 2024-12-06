from yt_concate.pipeline.pipeline import Pipeline
from yt_concate.pipeline.steps.download_videos import DownloadVideos
from yt_concate.pipeline.steps.edit_video import EditVideo
from yt_concate.pipeline.steps.get_video_list import GetVideoList
from yt_concate.pipeline.steps.download_captions import DownloadCaptions
from yt_concate.pipeline.steps.initialize_yt import InitializeYT
from yt_concate.pipeline.steps.postflight import Postflight
from yt_concate.pipeline.steps.preflight import Preflight
from yt_concate.pipeline.steps.read_captions import ReadCaptions
from yt_concate.pipeline.steps.search import Search
from yt_concate.utils import Utils

import sys, getopt
import logging

CHANNEL_ID = 'UCKSVUHI9rbbkXhvAXK-2uxA'

def print_usage():
    print('python main.py -s <search_word> -l <limit>')
    print('python main.py --search <search_word> --limit <limit>')

    print('python main.py OPTIONS')
    print('OPTIONS:')
    print('{:>6}{:<12}{}'.format('-c', '--channel', 'Channel ID of the YouTube channel.'))
    print('{:>6}{:<12}{}'.format('-s', '--search', 'The word will be searched for.'))
    print('{:>6}{:<12}{}'.format('-l', '--limit', 'Maximum combine count'))

def main():
    steps = [
        Preflight(),
        GetVideoList(),
        InitializeYT(),
        DownloadCaptions(),
        ReadCaptions(),
        Search(),
        DownloadVideos(),
        EditVideo(),
        Postflight(),
    ]

    short_opts = 'hc:s:l:'
    long_opts = 'channel= search= limit= cleanUp= fast= loggingLevel='.split()

    try:
        opts, args = getopt.getopt(sys.argv[1:], short_opts, long_opts)
    except getopt.GetoptError as err:
        # print help information and exit:
        print(err)  # will print something like "option -a not recognized"
        print_usage()
        sys.exit(2)

    channel_id = CHANNEL_ID
    search_word = ''
    limit = 70
    cleanUp = False
    fast = True
    loggingLevel = logging.WARNING

    for o, a in opts:
        if o == '-h':
            print_usage()
            sys.exit(0)
        elif o in ('-c', '--channel'):
            channel_id = a
        elif o in ('-s', '--search'):
            search_word = a
        elif o in ('-l', '--limit'):
            limit = a
        elif o == '--cleanUp':
            cleanUp = a
        elif o == '--fast':
            fast = a
        elif o == 'loggingLevel':
            loggingLevel = a
        else:
            print_usage()
            sys.exit(2)

    if not search_word or not limit:
        print_usage()
        sys.exit(2)

    inputs = {
        'channel_id': channel_id,
        'search_word': search_word,
        'limit': limit,
        'cleanUp': cleanUp, #結果檔產生後，刪除程式執行中產生的檔案，如下載的影片/字幕等
        'fast': fast, #True(預設)：程式執行中會先檢查檔案(包括影片、字幕) 有沒有已經存在電腦上，如果有則跳過，不重複下載
                      #False：強迫每次執行一定重新下載所有需要的檔案
        'loggingLevel': loggingLevel,
    }

    utils = Utils()
    p = Pipeline(steps)
    p.run(inputs, utils)


if __name__ == '__main__':
    main()
