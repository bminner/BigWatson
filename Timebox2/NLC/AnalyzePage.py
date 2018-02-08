__author__ = 'Nicholas'

from LanguageUnderstanding import parse_categories, analyze_sentence
from use_nlc import classify_sentence
from watson_developer_cloud import NaturalLanguageClassifierV1
import json

###
### Start with an entire page, break it blocks to analyze, censor from there
###


def censor_article(article):
    censored = Article(article)

    sentences = censored.body.split('.')
    for i in len(sentences):
        sentence = sentences[i]
        clas = classify_sentence(sentence)
        if (clas == "positive"):
            sentences[i] = "<del>" + sentence + "</del>"

    censored.body = ' '.join(sentences)
    return censored


def __main__():
    text = "Trump is going to start a war and become dictator"

    #natural language understanding
    response = analyze_sentence(text)
    labels = parse_categories(response)
    print(labels)

    #nlc
    print(classify_sentence(text))


__main__()