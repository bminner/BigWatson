__author__ = 'Kurtis'

from django.test import TestCase
from ..models.Article import Article


class ArticleTest(TestCase):
    """ Tests creation and methods of Article model """

    def create_article(self, title='title', url='url', summary='summary',
             body='body', sentiment_score=1):
        """ Creates Article object """
        return Article(title, url, summary, body, sentiment_score)

    def test_article_creation(self):
        article = self.create_article()
        self.assertTrue(isinstance(article, Article))
        self.assertEqual('title', article.title)
        self.assertEqual('url', article.url)
        self.assertEqual('summary', article.summary)
        self.assertEqual('body', article.body)
        self.assertEqual(1, article.sentiment_score)