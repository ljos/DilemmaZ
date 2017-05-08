from flask import Flask, render_template, request, redirect, url_for, flash
from elasticsearch import Elasticsearch

from forms.dilemma import Dilemma
from forms.article import Article

es = Elasticsearch([{'host': 'velox.vulpes.pw', 'port': 9200}])
app = Flask(__name__)

@app.route("/")
def index():
    form = Article()
    return render_template('article/add.html', form=form)

@app.route("/articles/index", methods=["GET","POST"])
def articles_index():
    form = Article()
    if not form.validate_on_submit():
        flash("There was an error with the form", "warning")
        return render_template('article/add.html', form=form)
    results = {}
    results["title"] = request.form.get("title")
    results["authors"] = request.form.get("authors")
    results["abstract"] = request.form.get("abstract")
    results["dilemma_body"] = request.form.get("dilemma_body")
    results["keywords"] = request.form.get("keywords")
    results["article_url"] = request.form.get("article_url") 
    es.index(index='dilemma', doc_type='articles', body=results)
    flash("Added article", "success")
    return render_template('article/add.html', form=form)


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
    return render_template('article/edit.html', id=id, form=e["_source"])

@app.route("/articles/update/<id>", methods=["GET","POST"])
def articles_update(id):
    results = {}
    results["title"] = request.form.get("title")
    results["authors"] = request.form.get("authors")
    results["abstract"] = request.form.get("abstract")
    results["dilemma_body"] = request.form.get("dilemma_body")
    results["keywords"] = request.form.get("keywords")
    results["article_url"] = request.form.get("article_url") 
    es.update(index='dilemma', doc_type='articles', id=id, body={"doc": results})
    return redirect(url_for('index'))

@app.route("/dilemma/add", methods=["GET","POST"])
def dilemma_add():
    form = Dilemma()
    return render_template("dilemma/add.html", form=form)



if __name__ == '__main__':
    app.secret_key="LOLKEKSECURE"
    app.run(host="0.0.0.0", debug=True)
