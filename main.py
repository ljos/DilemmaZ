import json

from collections import OrderedDict

from flask import Flask, render_template, request, redirect, url_for, flash
from elasticsearch import Elasticsearch
from forms.article import Article

es = Elasticsearch([{'host': 'velox.vulpes.pw', 'port': 9200}])
app = Flask(__name__)
app.config['WTF_CSRF_ENABLED'] = False
app.secret_key="LOLKEKSECURE"

@app.route("/")
def index():
    return redirect(url_for('articles_all'))

@app.route("/articles/index", methods=["GET","POST"])
def articles_index():
    form = Article()
    if request.method == 'POST' and not form.validate():
        flash("There was an error with the form", "warning")
        return render_template('article/add.html', form=form)

    if not form.validate_on_submit():
        if form.errors:
            flash("There was an error", "warning")
        return render_template('article/add.html', form=form)

    results = {}
    results["title"] = request.form.get("title")
    results["authors"] = request.form.get("authors")
    results["dilemma_body"] = request.form.get("dilemma_body")
    results["article_url"] = request.form.get("article_url") 
    results["logic"] = request.form.get("logic")
    results["feature"] = request.form.get("feature")
    results["actions"] = request.form.get("actions")
    results["case"] = request.form.get("case")
    results["duty_values"] = request.form.get("duty_values")
    es.index(index='dilemma', doc_type='articles', body=results)
    flash("Added article", "success")
    return render_template('article/add.html', form=form)

def _format_hit(hits):
    source = hits["_source"]
    source["id"] = hits["_id"]
    source["type"] = hits["_type"]
    if source["logic"]:
        source["logic"] = [i for i in source["logic"].split("\r\n")] 
    else:
        source["logic"] = []
    if source["feature"]:
        source["feature"] = [i for i in source["feature"].split("\r\n")] 
    else:
        source["feature"] = []
    if source["duty_values"]:
        source["duty_values"] = [i for i in source["duty_values"].split("\r\n")]
    else:
        source["duty_values"] = []

    if source["actions"]:
        source["actions"] = [i for i in source["actions"].split("\r\n")]
    else:
        source["actions"] = []
    return source

def _render_hits(results):
    # We really want everyting on newlines
    ret = []
    for hits in results:
        source = _format_hit(hits)
        ret.append(source)
    return ret

@app.route("/articles/search", methods=["GET","POST"])
def articles_search():
    results = []
    term = request.form.get("search")
    e = es.search(index="dilemma", body={
            "query": {
                "multi_match": {
                        "query": term,
                        "fields": [ "title", "authors",
                            "dilemma_body","article_url","logic","feature","actions","case","duty_values" ],
                        "fuzziness": "AUTO"
                    }
                }
            })
    results = _render_hits(e["hits"]["hits"])
    return render_template('search_results.html', results=results)


@app.route("/articles/all")
def articles_all():
    e = es.search(index="dilemma", doc_type="articles", body={"query": {"match_all": {}}})
    results = _render_hits(e["hits"]["hits"])
    return render_template('search_results.html', results=results)

def json_response(func):
    from functools import wraps

    @wraps(func)
    def wrapped(*args, **kwargs):
        response = func(*args, **kwargs)
        dump = json.dumps(response, indent=2, sort_keys=False)
        return dump, 200, {'Content-Type': 'application/json; charset=utf-8'}
    return wrapped

@app.route("/articles/all/json")
@json_response
def articles_all_json():
    e = es.search(index="dilemma", doc_type="articles", body={"query": {"match_all": {}}})
    results = _render_hits(e["hits"]["hits"])
    json = []
    for result in results:
        json.append(OrderedDict(sorted(result.items(), key=lambda t: t[0])))
    return json

@app.route("/article/<id>/json")
@json_response
def article_json(id):
    e = es.get(index="dilemma", doc_type="articles", id=id)
    results = _format_hit(e)
    return [results]

@app.route("/articles/edit/<id>", methods=["GET","POST"])
def articles_edit(id):
    e = es.get(index="dilemma", doc_type="articles", id=id)
    data = e["_source"]
    form = Article()
    if not form.is_submitted():
        form.title.data = data["title"]
        form.authors.data = data["authors"]
        form.dilemma_body.data = data["dilemma_body"]
        form.article_url.data = data["article_url"]
        form.logic.data = data["logic"]
        form.feature.data = data["feature"]
        form.actions.data = data["actions"]
        form.case.data = data["case"]
        form.duty_values.data = data["duty_values"]

    if not form.validate_on_submit():
        if form.errors:
            flash("There was an error", "warning")
        return render_template('article/edit.html', id=id, form=form)

    results = {}
    results["title"] = request.form.get("title")
    results["authors"] = request.form.get("authors")
    results["dilemma_body"] = request.form.get("dilemma_body")
    results["article_url"] = request.form.get("article_url") 
    results["logic"] = request.form.get("logic")
    results["feature"] = request.form.get("feature")
    results["actions"] = request.form.get("actions")
    results["case"] = request.form.get("case")
    results["duty_values"] = request.form.get("duty_values")

    es.update(index='dilemma', doc_type='articles', id=id, body={"doc": results})
    flash("Updated article", "success")
    return redirect(url_for('articles_edit', id=id))

@app.route("/articles/delete/<id>")
def articles_delete(id):
    es.delete(index='dilemma', doc_type='articles', id=id)
    flash("Deleted article", "success")
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
