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
    """Analyzes the given DocTree and returns a generator of Entity objects. """
    assert(isinstance(doctree, DocTree))

    title = doctree.original_title
    summary = doctree.original_summary
    body = doctree.original_body
    title_entities = _parse_entities(_query_nlu(title), doctree.title_word_at) if len(title) >= MIN_TEXT_LENGTH else []
    summary_entities = _parse_entities(_query_nlu(summary), doctree.summary_word_at) if len(summary) >= MIN_TEXT_LENGTH else []
    body_entities = _parse_entities(_query_nlu(body), doctree.body_word_at) if len(body) >= MIN_TEXT_LENGTH else []

    return AnalyzeResult(title_entities, summary_entities, body_entities)


def _query_nlu(text):
    """Responsible for the actual Watson NLU call"""
    return nlu.analyze(
        text=text,
        features=Features(
            entities=EntitiesOptions(
                sentiment=True,
                mentions=True,
                limit=20),
            semantic_roles=SemanticRolesOptions(limit=100, entities=True, keywords=True)
        )
    )


def _parse_entities(response, word_lookup_func):
    """Given JSON response from NLU query, replace mentions with proper WordNode and construct Entities"""
    print(json.dumps(response, sort_keys=True, indent=4))

    if 'entities' in response:

        # for each entity found
        for e in response['entities']:

            # extract info
            name = e['text']
            ttype = e['type']
            score = e['sentiment']['score']

            # optional mentions (sometimes none)
            if 'mentions' in e:
                mentions = [_parse_mention(m, word_lookup_func) for m in e['mentions']] if 'mentions' in e else []

            # initialize stuff for phrases
            mention_index = 0
            phrases = []

            # for each sentence in semantic_roles array
            for s in response['semantic_roles']:
                # if sentence has subject entities and it is the entity we want
                # OR if sentence has object entities and it is the entity we want
                # print(json.dumps(s, sort_keys=True, indent=4))
                if ('object' in s and 'entities' in s['subject'] and len(s['subject']['entities']) > 0 and s['subject']['entities'][0]['text'] == name) \
                        or ('object' in s and 'entities' in s['object'] and len(s['object']['entities']) > 0 and s['object']['entities'][0]['text'] == name):
                    # if valid mentions for that entity are available and mention text is found in subject or object
                    if mention_index < len(mentions) and (mentions[mention_index][0] in s['subject']['text'] or mentions[mention_index][0] in s['object']['text']):
                        mentions[mention_index] = (mentions[mention_index][0], mentions[mention_index][1], True)
                        phrases.append(s['object']['text'] + ' ' + s['subject']['text'])
                        mention_index += 1

            # clear mentions that had no corresponding phrase
            mentions = list(filter(lambda mention: mention[2], mentions))

            yield Entity(name, ttype, score, mentions, phrases)


def _parse_mention(m, word_lookup_func):
    """Replace integer location in mention with WordNode"""
    text = m['text']
    location = m['location']
    word = word_lookup_func(location[0])
    assert(word is not None) # This should not happen; implies that NLU gave us a bad location value
    return (text, word, False)


class AnalyzeResult:
    """Compilation of all Entities for one Article"""
    def __init__(self, title_entities, summary_entities, body_entities):
        self.title_entities = title_entities
        self.summary_entities = summary_entities
        self.body_entities = body_entities


class Entity:
    """Important noun in Article"""
    def __init__(self, name, ttype, sentiment_score, mentions, phrases):
        self.name = name
        self.type = ttype
        self.sentiment_score = sentiment_score
        self.mentions = mentions
        self.phrases = phrases

    def __repr__(self):
        return 'Name: {0} | Type: {1} | Sentiment: {2} | Mentions: {3} | Phrases: {4}'.format(
            self.name, self.type, self.sentiment_score, self.mentions, self.phrases)
