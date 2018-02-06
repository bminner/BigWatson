class Article:
    """ Container object for Discovery result """

    def __init__(self, title='', url='', summary='', body='', sentiment_score=0):
        self.title = title
        self.url = url
        self.summary = summary
        self.body = body
        self.sentiment_score = sentiment_score

    def get_title(self):
        return self.title

    def get_url(self):
        return self.url

    def get_summary(self):
        return self.summary

    def get_body(self):
        return self.body

    def get_sentiment_score(self):
        return self.sentiment_score
