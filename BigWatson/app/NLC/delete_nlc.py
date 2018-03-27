__author__ = 'Nicholas'

import requests
import json
from watson_developer_cloud import NaturalLanguageClassifierV1


def delete_api(classifier_id):
    nlu = NaturalLanguageClassifierV1(
        username='4d49cfca-bcdc-4ed9-a673-5d561faac440',
        password='GbojuhoOT5rG')

    nlu.delete_classifier(classifier_id)
    print('dead')


def __main__():
    delete_api('719667x294-nlc-224')


__main__()