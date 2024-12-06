from .step import Step


class ReadCaptions(Step):
    def process(self, data, inputs, utils):

        for yt in data:
            if not utils.caption_file_exists(yt):
                continue

            captions = {}
            with open(utils.get_caption_srt_path(yt), 'r', encoding="utf-8") as f:
                time_line = False
                time = None
                caption = None
                for line in f:
                    line = line.strip()
                    if '-->' in line:
                        time_line = True
                        time = line
                        continue
                    if time_line:
                        caption = line
                        captions[caption] = time
                        time_line = False
            yt.captions = captions

        return data
