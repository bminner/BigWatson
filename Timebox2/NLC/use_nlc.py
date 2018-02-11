__author__ = 'Nicholas'

from watson_developer_cloud import NaturalLanguageClassifierV1
import json


def classify_sentence(text):
    CLASSIFIER_ID = '719427x293-nlc-242'

    natural_language_classifier = NaturalLanguageClassifierV1(
    username='4d49cfca-bcdc-4ed9-a673-5d561faac440',
    password='GbojuhoOT5rG')

    #toy classifier
    #classes = natural_language_classifier.classify('33badcx272-nlc-24212', 'catastrophic')

    #real classifier
    classes = natural_language_classifier.classify(CLASSIFIER_ID, text)
    return json.dumps(classes, indent=2)


def __main__():
    text = "i love you"

    print(classify_sentence(text))


__main__()