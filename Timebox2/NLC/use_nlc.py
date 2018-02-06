__author__ = 'Nicholas'

from watson_developer_cloud import NaturalLanguageClassifierV1
import json

natural_language_classifier = NaturalLanguageClassifierV1(
    username='4d49cfca-bcdc-4ed9-a673-5d561faac440',
    password='GbojuhoOT5rG')

classes = natural_language_classifier.classify('33badcx272-nlc-24212', 'catastrophic')
print(json.dumps(classes, indent=2))