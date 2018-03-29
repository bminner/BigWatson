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

    text = 'The Ohio State University is  a great place to go to school. The Buckeyes have a great football team led by Urban Meyer. He is a good coach.'

    #try:
    """Analyzes the given text and returns a generator of Entity objects."""
    response = nlu.analyze(
        text=text,
        features=Features(
            entities=EntitiesOptions(
                sentiment=True,
                mentions=True,
                limit=20),
            semantic_roles=SemanticRolesOptions(limit=100, entities=True, keywords=True)
        )
    )
    #except Exception:
    #    print("\n\nProbably not enough text for language exception\n\n")

    return _parse_entities(response)


def _parse_entities(response):

    # print(json.dumps(response, sort_keys=True, indent=4))
    # print(response['entities'])
    for e in response['entities']:
        name = e['text']
        ttype = e['type']
        score = e['sentiment']['score']
        mentions = [(m['text'], m['location'], False) for m in e['mentions']]
        mention_index = 0
        phrases = []

        for s in response['semantic_roles']:
            #print('\n\n')
            #print(name)
            #print(json.dumps(s, sort_keys=True, indent=4))
            #print('\n\n')
            if 'entities' in s['subject'] and s['subject']['entities'][0]['text'] == name:
                #print('\n\nHERE\n\n')
                #print(mentions[mention_index])
                #print(s['subject']['text'])
                if mentions[mention_index][0] in s['subject']['text']:
                    mentions[mention_index] = (mentions[mention_index][0], mentions[mention_index][1], True)
                    phrases.append(s['object']['text'])
                    mention_index += 1

        mentions = list(filter(lambda mention: mention[2], mentions))

        print(Entity(name, ttype, score, mentions, phrases))

        yield Entity(name, ttype, score, mentions, phrases)


class Entity:
    def __init__(self, name, ttype, sentiment_score, mentions, phrases):
        self.name = name
        self.type = ttype
        self.sentiment_score = sentiment_score
        self.mentions = mentions
        self.phrases = phrases

    def __repr__(self):
        return 'Name: {0} | Type: {1} | Sentiment: {2} | Mentions: {3} | Phrases: {4}'.format(
            self.name, self.type, self.sentiment_score, self.mentions, self.phrases)
