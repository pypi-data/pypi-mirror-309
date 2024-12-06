class Found:
    def __init__(self, yt, caption, time):
        self.yt = yt
        self.caption = caption
        self.time = time

    def __str__(self):
        return '<Found(yt='+str(self.yt)+')>\n'

    def __repr__(self):
        content = ' : '.join([
            '\nyt=' + str(self.yt),
            '\ncaption=' + str(self.caption),
            '\ntime=' + str(self.time)
        ])
        return '<Found(' + content + ')>'
