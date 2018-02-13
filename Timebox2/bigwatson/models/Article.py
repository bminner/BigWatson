class Article:
    """ Container object for Discovery result """

    def __init__(self, title='', url='', summary='', body='', sentiment_score=0):
        self.title = title
        self.url = url
        self.summary = summary
        self.body = body
        self.sentiment_score = sentiment_score

    @classmethod
    def from_article(cls, art):
        return cls(title=art.title,
                        url=art.url,
                        summary=art.summary,
                        body=art.body,
                        sentiment_score=art.sentiment_score)
