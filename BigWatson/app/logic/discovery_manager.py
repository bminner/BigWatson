__author__ = 'Kurtis'

from ..models.Article import Article
from ..logic.helpers import QueryHelper
from ..logic import censor_manager
from watson_developer_cloud import DiscoveryV1
from goose3 import Goose


DISC_COLLECTION_ID = "news-en"
DISC_ENVIRONMENT_ID = "system"
discovery = DiscoveryV1(
    username="9ff594a4-6598-4609-9a46-3198a82ba99f",
    password="ACqN2zl6r5sz",
    version="2017-11-07"
)

def query_discovery_count(query, num):
    """ Returns a list of Articles by querying the Discovery service """

    discovery_query = discovery.query(environment_id=DISC_ENVIRONMENT_ID,
                                     collection_id=DISC_COLLECTION_ID,
                                     natural_language_query=query,
                                     return_fields=['title', 'url', 'enriched_text.sentiment.document.score'],
                                     count=num)

    # build QueryHelper with Goose extractor
    goose_extractor = Goose({'strict':False})
    qh = QueryHelper(goose_extractor)

    discovery_results = qh.parse_discovery_results(discovery_query['results'])

    return discovery_results


def query_discovery(query):
    """ Returns a list of Articles by querying the Discovery service """

    discovery_query = discovery.query(environment_id=DISC_ENVIRONMENT_ID,
                                     collection_id=DISC_COLLECTION_ID,
                                     natural_language_query=query,
                                     return_fields=['title', 'url', 'enriched_text.sentiment.document.score'],
                                     count=5)

    # build QueryHelper with Goose extractor
    goose_extractor = Goose({'strict':False})
    qh = QueryHelper(goose_extractor)

    discovery_results = qh.parse_discovery_results(discovery_query['results'])

    return discovery_results
