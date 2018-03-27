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
    """Analyzes the given text and returns a generator of Entity objects."""
    response = nlu.analyze(
        text=text,
        features=Features(
            entities=EntitiesOptions(
                sentiment=True,
                mentions=True,
                limit=20),
            semantic_roles=SemanticRolesOptions(limit=10)
        )
    )

    return _parse_entities(response)


def _parse_entities(response):
    entities = response['entities'] if 'entities' in response else []
    for e in entities:
        name = e['text']
        ttype = e['type']
        score = e['sentiment']['score']
        mentions = [(m['text'], m['location']) for m in e['mentions']] if 'mentions' in e else []
        yield Entity(name, ttype, score, mentions)


class Entity:
    def __init__(self, name, ttype, sentiment_score, mentions):
        self.name = name
        self.type = ttype
        self.sentiment_score = sentiment_score
        self.mentions = mentions

    def __repr__(self):
        return 'Name: {0} | Type: {1} | Sentiment: {2} | Mentions: {3}'.format(
            self.name, self.type, self.sentiment_score, self.mentions)
