from watson_developer_cloud.natural_language_understanding_v1 import *
from ..models import Article
from ..logic.doctree import DocTree, LinkedIndex
from watson_developer_cloud import NaturalLanguageUnderstandingV1
import json

MIN_TEXT_LENGTH = 50

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

def analyze(doctree):
    """ Analyzes the given DocTree and returns a generator of Entity objects. """
    assert(isinstance(doctree, DocTree))

    title = doctree.get_title()
    summary = doctree.get_summary()
    body = doctree.get_body()
    title_entities = _parse_entities(_query_nlu(title), doctree.title_word_at) if len(title) >= MIN_TEXT_LENGTH else []
    summary_entities = _parse_entities(_query_nlu(summary), doctree.summary_word_at) if len(summary) >= MIN_TEXT_LENGTH else []
    body_entities = _parse_entities(_query_nlu(body), doctree.body_word_at) if len(body) >= MIN_TEXT_LENGTH else []

    return AnalyzeResult(title_entities, summary_entities, body_entities)

def _query_nlu(text):
    return nlu.analyze(
        text=text,
        features=Features(
            entities=EntitiesOptions(
                sentiment=True,
                mentions=True,
                limit=20),
            semantic_roles=SemanticRolesOptions(limit=10)
        )
    )

def _parse_entities(response, word_lookup_func):
    entities = response['entities'] if 'entities' in response else []
    for e in entities:
        name = e['text']
        ttype = e['type']
        score = e['sentiment']['score']
        mentions = [_parse_mention(m, word_lookup_func) for m in e['mentions']] if 'mentions' in e else []
        yield Entity(name, ttype, score, mentions)

def _parse_mention(m, word_lookup_func):
    text = m['text']
    location = m['location']
    word = word_lookup_func(location[0])
    assert(word is not None) # This should not happen; implies that NLU gave us a bad location value
    return (text, word)

class AnalyzeResult:
    def __init__(self, title_entities, summary_entities, body_entitites):
        self.title_entities = title_entities
        self.summary_entities = summary_entities
        self.body_entitites = body_entitites

class Entity:
    def __init__(self, name, ttype, sentiment_score, mentions):
        self.name = name
        self.type = ttype
        self.sentiment_score = sentiment_score
        self.mentions = mentions

    def __repr__(self):
        return 'Name: {0} | Type: {1} | Sentiment: {2} | Mentions: {3}'.format(
            self.name, self.type, self.sentiment_score, self.mentions)
