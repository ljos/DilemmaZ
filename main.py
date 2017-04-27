from flask import Flask, render_template, request, redirect, url_for
from elasticsearch import Elasticsearch

es = Elasticsearch([{'host': 'velox.vulpes.pw', 'port': 9200}])
app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/articles/index", methods=["GET","POST"])
def articles_index():
    print(request.form)
    results = {}
    results["title"] = request.form.get("title")
    results["authors"] = request.form.get("authors")
    results["abstract"] = request.form.get("abstract")
    results["dilemma_body"] = request.form.get("dilemma_body")
    results["keywords"] = request.form.get("keywords")
    results["article_url"] = request.form.get("article_url") 
    es.index(index='dilemma', doc_type='articles', body=results)
    return render_template('index.html')


@app.route("/articles/search", methods=["GET","POST"])
def articles_search():
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


@app.route("/articles/all")
def articles_all():
    e = es.search(index="dilemma", body={"query": {"match_all": {}}})
    results = []
    print(e)
    for hits in e["hits"]["hits"]:
        doc = hits["_source"]
        doc["id"] = hits["_id"]
        results.append(doc)
    return render_template('search_results.html', results=results)

@app.route("/articles/edit/<id>")
def articles_edit(id):
    e = es.get(index="dilemma", doc_type="articles", id=id)
    return render_template('edit.html', id=id, form=e["_source"])

@app.route("/articles/update/<id>", methods=["GET","POST"])
def articles_update(id):
    print(id)
    results = {}
    results["title"] = request.form.get("title")
    results["authors"] = request.form.get("authors")
    results["abstract"] = request.form.get("abstract")
    results["dilemma_body"] = request.form.get("dilemma_body")
    results["keywords"] = request.form.get("keywords")
    results["article_url"] = request.form.get("article_url") 
    es.update(index='dilemma', doc_type='articles', id=id, body={"doc": results})
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
