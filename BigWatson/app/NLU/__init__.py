from ..models import Article
from watson_developer_cloud import NaturalLanguageUnderstandingV1
from watson_developer_cloud.natural_language_understanding_v1 import *

url = "https://gateway.watsonplatform.net/natural-language-understanding/api",
username = "5c878ccb-456a-433b-a8de-0f9e0dc41032"
password = "X8Bbn8WSMIDb"
nlu = NaturalLanguageUnderstandingV1(
    username=username,
    password=password,
    version='2017-02-27'
)
