import json, sys
from watson_developer_cloud import NaturalLanguageUnderstandingV1
from watson_developer_cloud.natural_language_understanding_v1 \
  import Features, EntitiesOptions, KeywordsOptions

natural_language_understanding = NaturalLanguageUnderstandingV1(
  username='9ba104e8-d9f9-4cdc-90b1-9bd2779b6fff',
  password='7dyryNUTyugc',
  version='2017-02-27')

def create_json_entities(site_url):
  response = natural_language_understanding.analyze(
    url=str(site_url),
    features=Features(
      entities=EntitiesOptions(
        sentiment=True,
        mentions=True,
        emotion=True,
        limit=1)))
  
  return response

response = create_json_entities(sys.argv[1])
with open('json-file.json', 'w') as json_file:
  json.dump(response, json_file, indent=2)
