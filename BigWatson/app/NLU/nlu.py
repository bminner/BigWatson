__author__ = 'Nicholas'

import json
from watson_developer_cloud import NaturalLanguageUnderstandingV1
from watson_developer_cloud.natural_language_understanding_v1 import *


url = "https://gateway.watsonplatform.net/natural-language-understanding/api",
username = "5c878ccb-456a-433b-a8de-0f9e0dc41032"
password = "X8Bbn8WSMIDb"


def analyze_sentence(text_to_analyze):
    nlu = NaturalLanguageUnderstandingV1(
        username=username,
        password=password,
        version='2017-02-27'
    )

    response = nlu.analyze(
        text=text_to_analyze,
        features=Features(
            entities=EntitiesOptions(
                emotion=True,
                sentiment=True,
                limit=10),
            keywords=KeywordsOptions(
                emotion=True,
                sentiment=True,
                limit=10),
            categories=CategoriesOptions()
        )
    )

    #print(json.dumps(response, indent=2))
    parse_categories(response)
    return response


def parse_categories(response):
    lab_to_score = {}
    labels = []
    for cat in response["categories"]:
        #lab_to_score[cat["label"]] = cat["score"]
        labels += (cat["label"][1:].split("/"))
    #print(lab_to_score)
    #print(labels)

    return labels #, lab_to_score not used currently


def __main__():
    text = "Donald Trump is a Bad Hombre"
    analyze_sentence(text)

__main__()
