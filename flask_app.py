from flask import Flask, jsonify, render_template
from db.database import db_session
from db.models import UsuariosRT, Termos, Hashtags, HashtagsGraph, UsuariosCitados, BigramTrigram, AllTweets
from sqlalchemy.sql.functions import func
import pytz
import datetime
import calendar
import configparser

from sqlalchemy import and_

app = Flask(__name__)
 

config = configparser.ConfigParser()
config.read("config.ini")

SIDE_A = config['GENERAL']['SIDE_A']
SIDE_B = config['GENERAL']['SIDE_B']
CONTEXT = config['GENERAL']['CONTEXT']
HASHTAG = config['GENERAL']['HASHTAG']

def change_fuso(value):

    fuso_horario = pytz.timezone("America/Sao_Paulo")
    date_ = value.replace(tzinfo=pytz.utc)
    date_ = date_.astimezone(fuso_horario)
    str_time = date_.strftime("%Y-%m-%d %H:%M:%S")

    return str_time

def format_datetime(value):

    fuso_horario = pytz.timezone("America/Sao_Paulo")
    date_ = value.replace(tzinfo=pytz.utc)
    date_ = date_.astimezone(fuso_horario)
    str_time = date_.strftime("%d/%m/%y %H:%M:%S")

    return str_time

app.jinja_env.filters['datetime'] = format_datetime

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


def load_from_db(limit=10):

    query_usuarios_rt = UsuariosRT.query.filter(UsuariosRT.context.is_(CONTEXT)).order_by(UsuariosRT.frequencia.desc()).limit(limit).all()
    query_termos = Termos.query.filter(Termos.context.is_(CONTEXT)).order_by(Termos.frequencia.desc()).limit(limit).all()
    query_hashtags = Hashtags.query.filter(Hashtags.context.is_(CONTEXT)).order_by(Hashtags.frequencia.desc()).limit(limit).all()
    query_usuarios_citados = UsuariosCitados.query.filter(UsuariosCitados.context.is_(CONTEXT)).order_by(UsuariosCitados.frequencia.desc()).limit(limit).all()

    query_bigram_trigram = BigramTrigram.query.filter(BigramTrigram.context.is_(CONTEXT)).order_by(BigramTrigram.frequencia.desc()).limit(limit).all()

    return query_termos, query_hashtags, query_usuarios_rt, query_usuarios_citados, query_bigram_trigram

@app.route("/")
def home():

    total_texts = db_session.query(func.count(AllTweets.id).label('total_texts')).filter(AllTweets.context.is_(CONTEXT)).first().total_texts

    if total_texts == 0:
        return("There is no data for this context: " + CONTEXT)

    total_terms = db_session.query(func.count(Termos.id).label('total_terms')).filter(Termos.context.is_(CONTEXT)).first().total_terms
    total_processed = db_session.query(func.count(AllTweets.id).label("total_processed")).filter(AllTweets.context.is_(CONTEXT)).filter(AllTweets.processed==1).first().total_processed
    

    date_max = db_session.query(AllTweets.id, func.max(AllTweets.date).label('last_date')).filter(AllTweets.context.is_(CONTEXT)).first().last_date
    date_min = db_session.query(AllTweets.id, func.min(AllTweets.date).label('last_date')).filter(AllTweets.context.is_(CONTEXT)).first().last_date

    termos, hashtags, usuarios_rt, usuarios_citados, bigram_trigram = load_from_db(10)

    if HASHTAG == "True":
        query_a = Hashtags.query.filter(and_(Hashtags.hashtag.is_(SIDE_A),Hashtags.context.is_(CONTEXT))).first()
        query_b = Hashtags.query.filter(and_(Hashtags.hashtag.is_(SIDE_B),Hashtags.context.is_(CONTEXT))).first()
    else:
        query_a = Termos.query.filter(and_(Termos.termo.is_(SIDE_A),Termos.context.is_(CONTEXT))).first()
        query_b = Termos.query.filter(and_(Termos.termo.is_(SIDE_B),Termos.context.is_(CONTEXT))).first()

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
        'total_texts': total_texts,
        'total_terms': total_terms,
        'total_processed': total_processed,
        'date_max': date_max,
        'date_min': date_min,
        'side_a': SIDE_A,
        'side_b': SIDE_B,
        'termos': termos,
        'hashtags': hashtags,
        'usuarios_rt': usuarios_rt,
        'usuarios_citados': usuarios_citados,
        'total': (percent_a, percent_b),
        'total_value': (int(total_a), int(total_b)),
        'bigram_trigram': bigram_trigram,
        'context': CONTEXT

    }


    return render_template("index.html",values=dict_values)


@app.route("/graph/")
def graph():

    query_hashtag = HashtagsGraph.query.filter_by(context=CONTEXT).all()
    all_ = []

    fuso_horario = pytz.timezone("America/Sao_Paulo")

    for q in query_hashtag:

        
        date_ = change_fuso(q.date)

        
        
        t = {}
        t['date'] = date_
        t['count'] = q.frequencia
        t['hashtag'] = q.hashtag
        all_.append(t)

    return jsonify(**{'list': all_})


@app.route("/cloud/")
def cloud():

    query_termos = Termos.query.filter(Termos.context.is_(CONTEXT)).order_by(Termos.frequencia.desc()).limit(400).all()

    t = {}

    for q in query_termos:
        if q.termo != SIDE_A and q.termo != SIDE_B:
            t[q.termo] = q.frequencia

    return jsonify(**t)


if __name__ == "__main__":
    app.debug = True
    app.run()
