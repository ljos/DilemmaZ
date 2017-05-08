from flask import Flask, render_template, request, redirect, url_for, flash
from elasticsearch import Elasticsearch
import json

from forms.dilemma import Dilemma
from forms.article import Article

es = Elasticsearch([{'host': 'velox.vulpes.pw', 'port': 9200}])
app = Flask(__name__)
app.config['WTF_CSRF_ENABLED'] = False

@app.route("/")
def index():
    form = Article()
    return render_template('article/add.html', form=form)

@app.route("/articles/index", methods=["GET","POST"])
def articles_index():
    form = Article()
    if request.method == 'POST' and not form.validate():
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
                        "fields": [ "title", "authors", "abstract", "dilemma_body", "name","dilemma" ],
                        "fuzziness": "AUTO"
                    }
                }
            })
    for hits in e["hits"]["hits"]:
        source = hits["_source"]
        source["type"] = hits["_type"]
        results.append(source)
    print(source)
    return render_template('search_results.html', results=results)


@app.route("/articles/all")
def articles_all():
    e = es.search(index="dilemma", doc_type="articles", body={"query": {"match_all": {}}})
    results = []
    for hits in e["hits"]["hits"]:
        doc = hits["_source"]
        doc["id"] = hits["_id"]
        doc["type"] = hits["_type"]
        results.append(doc)
    return render_template('search_results.html', results=results)

@app.route("/articles/edit/<id>", methods=["GET","POST"])
def articles_edit(id):
    e = es.get(index="dilemma", doc_type="articles", id=id)
    data = e["_source"]
    form = Article()
    if not form.is_submitted():
        form.title.data = data["title"]
        form.authors.data = data["authors"]
        form.abstract.data = data["abstract"]
        form.dilemma_body.data = data["dilemma_body"]
        form.keywords.data = data["keywords"]
        form.article_url.data = data["article_url"]

    if not form.validate_on_submit():
        if form.errors:
            flash("There was an error", "warning")
        return render_template('article/edit.html', id=id, form=form)

    results = {}
    results["title"] = request.form.get("title")
    results["authors"] = request.form.get("authors")
    results["abstract"] = request.form.get("abstract")
    results["dilemma_body"] = request.form.get("dilemma_body")
    results["keywords"] = request.form.get("keywords")
    results["article_url"] = request.form.get("article_url") 

    es.update(index='dilemma', doc_type='articles', id=id, body={"doc": results})
    flash("Updated article", "success")
    return redirect(url_for('index'))


@app.route("/dilemma/index", methods=["GET","POST"])
def dilemma_add():
    form = Dilemma()
    if not form.is_submitted():
        return render_template('dilemma/add.html', form=form)
    if request.method == 'POST' and not form.validate():
        flash("There was an error with the form", "warning")
        return render_template('dilemma/add.html', form=form)
    results = {}
    results["name"] = request.form.get("name")
    results["dilemma"] = request.form.get("dilemma")
    es.index(index='dilemma', doc_type='dilemma', body=results)
    flash("Added dilemma", "success")
    return redirect(url_for('index'))

@app.route("/dilemma/all")
def dilemma_all():
    e = es.search(index="dilemma", doc_type="dilemma", body={"query": {"match_all": {}}})
    results = []
    for hits in e["hits"]["hits"]:
        doc = hits["_source"]
        doc["id"] = hits["_id"]
        doc["type"] = hits["_type"]
        results.append(doc)
    return render_template('search_results.html', results=results)

@app.route("/dilemma/edit/<id>", methods=["GET","POST"])
def dilemma_edit(id):
    e = es.get(index="dilemma", doc_type="dilemma", id=id)
    data = e["_source"]
    form = Dilemma()
    if not form.is_submitted():
        form.name.data = data["name"]
        form.dilemma.data = data["dilemma"]

    if not form.validate_on_submit():
        if form.errors:
            flash("There was an error", "warning")
        return render_template('dilemma/edit.html', id=id, form=form)

    results = {}
    results["name"] = request.form.get("name")
    results["dilemma"] = request.form.get("dilemma")
    es.update(index='dilemma', doc_type='dilemma', id=id, body={"doc": results})
    flash("Updated dilemma", "success")
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.secret_key="LOLKEKSECURE"
    app.run(host="0.0.0.0", debug=True)
