__author__ = 'Kurtis'

from ..models.Article import Article
from ..logic.helpers import QueryHelper
from watson_developer_cloud import DiscoveryV1
from goose3 import Goose


#small news info
SMALL_COLLECTION_ID = "25ee1422-b190-4079-8f66-16e70dce7965"
SMALL_ENVIRONMENT_ID = "8023a435-96d1-451c-b68f-59ff11be5509"

small_discovery = DiscoveryV1(
    username="66c89b69-2cb7-4a74-b8c4-ed42c69bf258",
    password="fS6kFnMwBDSy",
    version="2017-11-07"
)


def query_discovery(query, count=5):
    """ Returns a list of Articles by querying the Discovery service """

    queries = ["Donald Trump", "North Korea", "Puppies", "Snakes", "France", "Nick Meyer", "Mexico"]
    if query in queries:
        print("USING SMALL NEWS")
        discovery_query = small_discovery.query(environment_id=SMALL_ENVIRONMENT_ID,
                                         collection_id=SMALL_COLLECTION_ID,
                                         natural_language_query=query,
                                         return_fields=['title', 'summary', 'url', 'body', 'sentiment_score'],
                                         count=count)
        results = discovery_query['results']

        discovery_results = []

        for result in results:
            title = result['title']
            url = result['url']

            summary = result['summary']
            body = result['body']
            sentiment_score = result['sentiment_score']

            discovery_results.append(Article(title, url, summary, body, sentiment_score))
    else:

        print("USING BIG NEWS")

        DISC_COLLECTION_ID = "news-en"
        DISC_ENVIRONMENT_ID = "system"
        discovery = DiscoveryV1(
            username="9ff594a4-6598-4609-9a46-3198a82ba99f",
            password="ACqN2zl6r5sz",
            version="2017-11-07"
        )

        discovery_query = discovery.query(environment_id=DISC_ENVIRONMENT_ID,
                                         collection_id=DISC_COLLECTION_ID,
                                         natural_language_query=query,
                                         return_fields=['title', 'url', 'enriched_text.sentiment.document.score'],
                                         count=count)

        # build QueryHelper with Goose extractor
        goose_extractor = Goose({'strict':False})
        qh = QueryHelper(goose_extractor)

        discovery_results = []
        if len(discovery_query['results']) > 0:
            discovery_results = qh.parse_discovery_results(discovery_query['results'])

    return discovery_results