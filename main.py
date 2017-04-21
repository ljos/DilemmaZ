from flask import Flask, render_template, request
from elasticsearch import Elasticsearch

es = Elasticsearch([{'host': 'velox.vulpes.pw', 'port': 9200}])
app = Flask(__name__)

@app.route("/")
def root():
    return render_template('index.html')

@app.route("/index_article", methods=["GET","POST"])
def index_article():
    results = {}
    results["title"] = request.form.get("title")
    results["authors"] = request.form.get("authors")
    results["abstract"] = request.form.get("abstract")
    results["dilemma_body"] = request.form.get("dilemma_body")
    results["keyword"] = request.form.get("keyword")
    results["article_url"] = request.form.get("article_url") es.index(index='dilemma', doc_type='articles', body=results)
    return "Probably works"

@app.route("/search", methods=["GET","POST"])
def search():
    results = []
    term = request.form.get("search")
    e = es.search(index="dilemma", body={
            "query": {
                "multi_match": {
                        "query": term,
                        "fields": [ "title", "authors", "abstract", "dilemma_body" ],
                        "fuzziness": "AUTO"
                    }
                }
            })
    for hits in e["hits"]["hits"]:
        results.append(hits["_source"])
    return render_template('search_results.html', results=results)


@app.route("/all")
def all():
    e = es.search(index="dilemma", body={"query": {"match_all": {}}})
    results = []
    for hits in e["hits"]["hits"]:
        results.append(hits["_source"])
    return render_template('search_results.html', results=results)

app.run()
