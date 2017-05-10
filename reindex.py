import json
from elasticsearch import Elasticsearch
es = Elasticsearch([{'host': 'velox.vulpes.pw', 'port': 9200}])

l = json.load(open("./articles"))

es.indices.delete(index='dilemma', ignore=[400, 404])

for i in l:

    results = {}
    results["title"] = i["title"]
    results["authors"] = i["authors"]
    results["dilemma_body"] = i["dilemma_body"]
    results["article_url"] = i["article_url"]
    results["logic"] = "" 
    results["feature"] = ""
    results["actions"] = ""
    results["case"] = "" 
    results["duty_values"] = ""
    es.index(index='dilemma', doc_type='articles', body=results)
