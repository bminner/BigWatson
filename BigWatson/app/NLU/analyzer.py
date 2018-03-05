from NLU import nlu
from watson_developer_cloud.natural_language_understanding_v1 import *

def analyze(text):
    """Analyzes the given text and returns a generator of Entity objects."""
    response = nlu.analyze(
        text=text,
        features=Features(
            entities=EntitiesOptions(
                sentiment=True,
                mentions=True,
                limit=100),
            semantic_roles=SemanticRolesOptions(limit=100)
        )
    )

    return _parse_entities(response)


def _parse_entities(response):
    entities = response['entities']
    for e in entities:
        name = e['text']
        ttype = e['type']
        score = e['sentiment']['score']
        mentions = [(m['text'], m['location']) for m in e['mentions']]
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
