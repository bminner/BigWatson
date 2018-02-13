__author__ = 'Nicholas'

import requests
import json
from watson_developer_cloud import NaturalLanguageClassifierV1


# {
#   "status": "Training",
#   "name": "Classifier Demo",
#   "language": "en",
#   "created": "2018-02-01T21:59:19.776Z",
#   "url": "https://gateway.watsonplatform.net/natural-language-classifier/api/v1/classifiers/33badcx272-nlc-24212",
#   "status_description": "The classifier instance is in its training phase, not yet ready to accept classify requests",
#   "classifier_id": "33badcx272-nlc-24212"
# }

# {
#   "created": "2018-02-08T21:37:07.878Z",
#   "language": "en",
#   "status": "Training",
#   "status_description": "The classifier instance is in its training phase, not yet ready to accept classify requests",
#   "classifier_id": "719427x293-nlc-242",
#   "url": "https://gateway.watsonplatform.net/natural-language-classifier/api/v1/classifiers/719427x293-nlc-242",
#   "name": "Pos Neg Class"
# }


def create_api(file_name):
    nlu = NaturalLanguageClassifierV1(
      username='4d49cfca-bcdc-4ed9-a673-5d561faac440',
      password='GbojuhoOT5rG')

    with open(file_name, 'rb') as training_data:
        classifier = nlu.create_classifier(
            training_data=training_data,
            metadata=json.dumps({'name': 'Pos Neg Class', 'language': 'en'})
        )

    print(json.dumps(classifier, indent=2))


def create_curl():

  ###DOESNT WORK

    url = "https://gateway.watsonplatform.net/natural-language-classifier/api/v1/classifiers"
    username = '4d49cfca-bcdc-4ed9-a673-5d561faac440'
    password = 'GbojuhoOT5rG'

    headers = {"Content-Type": "text/plain", "charset": "utf-8"}
    with open(file_name, 'rb') as training_data:
        data = {"training_data": training_data, "training_metadata": "{\"language\":\"en\",\"name\":\"Demo Classifier\"}"}

        r = requests.post(url, data=data, headers=headers, auth=(username, password))

    print(r.status_code)
    print(json.dumps(r.json(), indent=2))


def __main__():
    file_name = '../sentences/pos_neg_responses.csv'
    create_api(file_name)

__main__()


