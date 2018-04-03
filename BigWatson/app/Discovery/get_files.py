__author__ = 'Nicholas'

import string
import random
from ..logic import discovery_manager
from watson_developer_cloud import DiscoveryV1
import os
import json

#small news info
DISC_COLLECTION_ID = "25ee1422-b190-4079-8f66-16e70dce7965"
DISC_ENVIRONMENT_ID = "8023a435-96d1-451c-b68f-59ff11be5509"
discovery = DiscoveryV1(
    username="66c89b69-2cb7-4a74-b8c4-ed42c69bf258",
    password="fS6kFnMwBDSy",
    version="2017-11-07"
)


queries = ["donald trump", "north korea", "puppies", "snakes", "france"]

for query in queries:
    print(query)
    results = discovery_manager.query_discovery(query, 10)

    filenames = []
    for result in results:
        del_file = ""

        file_text = "{\n"\
                   "\"title\":\"" + result.title.replace("\"", "\\\"").replace("\n", "\\n").replace("\r", "\\n") + "\",\n"\
                   "\"summary\":\"" + result.summary.replace("\"", "\\\"").replace("\n", "\\n").replace("\r", "\\n") + "\",\n"\
                   "\"body\":\"" + result.body.replace("\"", "\\\"").replace("\n", "\\n").replace("\r", "\\n") + "\",\n"\
                   "\"url\":\"" + result.url + "\",\n"\
                   "\"sentiment_score\":\"" + str(result.sentiment_score) + "\"\n"\
                   "}"

        fname = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10)) + '.json'
        filenames.append(fname)
        with open(fname, 'w') as fout:
            try:
                fout.write(file_text)
            except UnicodeEncodeError:
                print("unicode shit")
                del_file = filenames.pop()

        if len(del_file) > 0:
            os.remove(del_file)
            del_file = ""

    print(filenames)
    for fname in filenames:
        with open(fname) as fileinfo:
          add_doc = discovery.add_document(DISC_ENVIRONMENT_ID, DISC_COLLECTION_ID, file=fileinfo)
        print(json.dumps(add_doc, indent=2))