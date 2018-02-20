__author__ = 'Kurtis'

from ..models.Article import Article


class QueryHelper:
    """
    Helper class initialized with extractor client to manage parsing and
    extracting Discovery result data.
    """

    def __init__(self, extractor_client):
        self.extractor = extractor_client

    def parse_discovery_results(self, results):
        """
        Parses results received from querying Watson Discovery.
        Returns list of Articles parsed from json results.
        """
        
        discovery_results = []
        for result in results:
            title = result['title']
            url = result['url']
            
            article_data = self.get_article_data(url)

            summary = article_data['summary']
            body = article_data['body']
            sentiment_score = result['enriched_text']['sentiment']['document']['score']

            discovery_results.append(Article(title, url, summary, body, sentiment_score))

        return discovery_results

    def get_article_data(self, url):
        """
        Extracts article data from provided url. Default extractor is Goose object.
        Returns dictionary of strings with keys summary and body.
        """

        # Extract article data
        article = self.extractor.extract(url=url)

        data = {'summary': '', 'body': ''}
        summary = article.meta_description
        body = article.cleaned_text

        # if no meta description, make summary first 200 characters of article body
        data['summary'] = summary if len(summary) > 0 else body[:200] + '...'
        data['body'] = article.cleaned_text.replace('\n', '</p><p>')

        return data
