from .step import Step

import logging

from moviepy.editor import VideoFileClip, concatenate_videoclips

class EditVideo(Step):
    def process(self, data, inputs, utils):
        logger = logging.getLogger()
        clips = []
        for found in data:
            logger.debug(found.time)
            start, end = self.parse_caption_time(found.time)
            video_clip = VideoFileClip(utils.get_video_real_filename(found.yt)).subclip(start, end)
            clips.append(video_clip)
            if len(clips) >= inputs['limit']:
                break
        final_clip = concatenate_videoclips(clips)
        output_filepath = utils.get_output_filepath(inputs['channel_id'], inputs['search_word'])
        final_clip.write_videofile(output_filepath)

        return

    def parse_caption_time(self, caption_time):
        start, end = caption_time.split(' --> ')
        return self.parse_time_str(start), self.parse_time_str(end)

    def parse_time_str(self, time_str):
        h, m, s = time_str.split(':')
        s, ms = s.split(',')
        return int(h), int(m), int(s)+int(ms)/1000

