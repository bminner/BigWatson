import json

def analyze_article(article):
    """Analyzes the given 'Article' and returns a generator of Entity objects."""
    response = nlu.analyze(
        url='http://www.newsweek.com/trump-worst-president-ever-thats-patently-absurd-814948',
        features=Features(
            entities=EntitiesOptions(
                sentiment=True,
                mentions=True,
                limit=100),
            semantic_roles=SemanticRolesOptions(limit=100)
        )
    )

    return self._parse_entities(response)


def _parse_entities(self, response):
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
