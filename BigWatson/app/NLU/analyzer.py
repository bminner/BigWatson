from watson_developer_cloud.natural_language_understanding_v1 import *
from ..models import Article
from watson_developer_cloud import NaturalLanguageUnderstandingV1
import json


def init_nlu_engine():
    url = "https://gateway.watsonplatform.net/natural-language-understanding/api",
    username = "5c878ccb-456a-433b-a8de-0f9e0dc41032"
    password = "X8Bbn8WSMIDb"
    return NaturalLanguageUnderstandingV1(
        username=username,
        password=password,
        version='2017-02-27'
        )

nlu = init_nlu_engine()

def analyze(text):
    response = {}
    #try:
    """Analyzes the given text and returns a generator of Entity objects."""
    response = nlu.analyze(
        text=text,
        features=Features(
            entities=EntitiesOptions(
                sentiment=True,
                mentions=True,
                limit=5),
            semantic_roles=SemanticRolesOptions(limit=10)
        )
    )
    #except Exception:
    #    print("\n\nProbably not enough text for language exception\n\n")

    with open('data.txt', 'w') as outfile:
        json.dump(response, outfile)

    return _parse_entities(response)


def _parse_entities(response):
    #try:
    entities = response['entities']
    for e in entities:
        name = e['text']
        ttype = e['type']
        score = e['sentiment']['score']
        mentions = [(m['text'], m['location']) for m in e['mentions']]
        yield Entity(name, ttype, score, mentions)
    #except KeyError:
    print("/n/nThere is apparently no entity of mentions in this article.")


class Entity:
    def __init__(self, name, ttype, sentiment_score, mentions):
        self.name = name
        self.type = ttype
        self.sentiment_score = sentiment_score
        self.mentions = mentions

    def __repr__(self):
        return 'Name: {0} | Type: {1} | Sentiment: {2} | Mentions: {3}'.format(
            self.name, self.type, self.sentiment_score, self.mentions)
