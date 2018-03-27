__author__ = 'Nicholas'

#from ..NLC.LanguageUnderstanding import parse_categories, analyze_sentence
from ..NLC.use_nlc import classify_sentence
from ..models import Article

from watson_developer_cloud import NaturalLanguageClassifierV1
import json

###
### Start with an entire page, break it blocks to analyze, censor from there
###
def censor_article(article):


    BAD_CLASS = 'negative'

    censored = Article.Article.from_article(article)

    sentences = censored.body.split('.')
    for i in range(len(sentences)):
        sentence = sentences[i]
        cls = ''
        pos_conf = 1
        if len(sentence) > 0:
            cls, pos_conf = classify_sentence(sentence)
            print(cls)
        if pos_conf < .33:
            try:
                print("Bad hombre:" + sentence)
            except UnicodeEncodeError:
                print("unicode shit")
            sentences[i] = '<del>' + sentence + '</del>'

    censored_body = ' '.join(sentences)
    censored.body = censored_body
    return censored
