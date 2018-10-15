from flask import Flask, jsonify, render_template
from db.database import db_session
from db.models import UsuariosRT, Termos, Hashtags, HashtagsGraph, UsuariosCitados, BigramTrigram

app = Flask(__name__)

SIDE_A = "haddad"
SIDE_B = "bolsonaro"
CONTEXT = "eleicoes2018"
HAHSTAG = False

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


def load_from_db(limit=10):

    query_usuarios_rt = UsuariosRT.query.order_by(UsuariosRT.frequencia.desc()).limit(limit).all()
    query_termos = Termos.query.order_by(Termos.frequencia.desc()).limit(limit).all()
    query_hashtags = Hashtags.query.order_by(Hashtags.frequencia.desc()).limit(limit).all()
    query_usuarios_citados = UsuariosCitados.query.order_by(UsuariosCitados.frequencia.desc()).limit(limit).all()

    query_bigram_trigram = BigramTrigram.query.all()

    return query_termos, query_hashtags, query_usuarios_rt, query_usuarios_citados, query_bigram_trigram

@app.route("/")
def home():

    termos, hashtags, usuarios_rt, usuarios_citados, bigram_trigram = load_from_db(10)

    if HAHSTAG:
        query_a = Hashtags.query.filter_by(hashtag=SIDE_A).first()
        query_b = Hashtags.query.filter_by(hashtag=SIDE_B).first()
    else:
        query_a = Termos.query.filter_by(termo=SIDE_A).first()
        query_b = Termos.query.filter_by(termo=SIDE_B).first()

    total_a = 0
    total_b = 0
    percent_a = 0
    percent_b = 0
    total = 0

    if query_a and query_b:
        total_a = float(query_a.frequencia)
        total_b = float(query_b.frequencia)

        total = total_a + total_b

        percent_a = (total_a / total) * 100
        percent_b = (total_b / total) * 100

    dict_values = {
        'side_a': SIDE_A,
        'side_b': SIDE_B,
        'termos': termos,
        'hashtags': hashtags,
        'usuarios_rt': usuarios_rt,
        'usuarios_citados': usuarios_citados,
        'total': (percent_a, percent_b),
        'bigram_trigam': bigram_trigram,
        'context': CONTEXT

    }


    return render_template("index.html",values=dict_values)


@app.route("/graph/")
def graph():

    query_hashtag = HashtagsGraph.query.filter_by(context=CONTEXT).all()
    all_ = []
    for q in query_hashtag:
        date_ = str(q.date)
        print(date_)
        t = {}
        t['date'] = date_
        t['count'] = q.frequencia
        t['hashtag'] = q.hashtag
        all_.append(t)

    return jsonify(**{'list': all_})


@app.route("/cloud/")
def cloud():

    query_termos = Termos.query.order_by(Termos.frequencia.desc()).limit(400).all()

    t = {}

    for q in query_termos:
        if q.termo != SIDE_A and q.termo != SIDE_B:
            t[q.termo] = q.frequencia

    return jsonify(**t)


if __name__ == "__main__":
    app.debug = True
    app.run()
