import json
from elasticsearch import Elasticsearch
es = Elasticsearch([{'host': 'velox.vulpes.pw', 'port': 9200}])

l = json.load(open("./articles"))

es.indices.delete(index='dilemma', ignore=[400, 404])

for i in l:
    es.index(index='dilemma', doc_type='articles', body=i)
