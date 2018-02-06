from ..models.Article import Article
from watson_developer_cloud import DiscoveryV1


DISC_COLLECTION_ID = "news-en"
DISC_ENVIRONMENT_ID = "system"
discovery = DiscoveryV1(
    username="9ff594a4-6598-4609-9a46-3198a82ba99f",
    password="ACqN2zl6r5sz",
    version="2017-11-07"
)

def query_discovery(query):
    """ Returns a list of Articles by querying the Discovery service """

    qopts = {'query': query, 'filter': query, 'count':5,
             'return': 'title, url, text, enriched_text.sentiment.document.score'}
    discovery_query = discovery.query(DISC_ENVIRONMENT_ID, DISC_COLLECTION_ID, qopts)
    discovery_results = []
    for result in discovery_query['results']:
        title = result['title']
        url = result['url']
        summary = clean_summary(result['text'], title)
        sentiment_score = result['enriched_text']['sentiment']['document']['score']

        discovery_results.append(Article(title, url, summary, sentiment_score=sentiment_score))

    return discovery_results

def clean_summary(text, title):
    """ Removes title and shortens summary from Discovery text result """
    summary = text.replace(title, '')
    summary = (summary[:160] + '...') if len(summary) > 160 else summary

    return summary

