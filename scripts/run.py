import sys
import os
import pytz

from collections import Counter
from nltk.tokenize import regexp_tokenize
from datetime import datetime

from .d2l_collector.collecting import Collecting
from .d2l_processing.processing import Processing
from db.models import AllTweets, UsuariosCitados, UsuariosRT, Hashtags, HashtagsGraph, Termos, BigramTrigram
from db.database import db_session

from unicodedata import normalize

collector = Collecting()
processor = Processing()

side_a = "haddad"
side_b = "bolsonaro"

# Ler tweets já gravados no banco de dados e retorna uma lista com os textos e com os usuários
def get_tweets_from_database(context=None):

    
    tweets = db_session.query(AllTweets).filter_by(context=context)
    

    list_text = []
    list_user = []
    list_rt_user = []

    for tweet in tweets:
        list_text.append(tweet.text)
        if tweet.rt_user != "":
            list_rt_user.append(tweet.rt_user)


    return list_text, list_rt_user

def start(context_=None):


    print("Processing Tweets ...")
    list_texts, list_rt_user = get_tweets_from_database(context=context_)
    final_words = processor.get_final_words(list_texts, False)
    frequency_terms = processor.get_frequence_terms(final_words)
    frequency_users_cited = processor.get_frequence_users_cited()
    frequency_users_cited_rt = processor.get_frequence_users_rt(list_rt_user)
    
    frequency_hashtags = processor.get_frequence_hashtags()
    bigrams, trigrams = processor.get_bigrams_trigrams(final_words)

    # Clearing Tables
    print("Cleaning database")
    clear_tables()

     # Insert in database
    print("Populating database")
    populate_database(bigrams, frequency_hashtags, frequency_terms, frequency_users_cited_rt, frequency_users_cited, trigrams)

    #Hashtags Graph
    print("Generating Hashtag count by date")
    hashtag_graph(context_)


def hashtag_graph(context_=None):

    tweets = db_session.query(AllTweets).filter_by(context=context_)

    pattern = r'(https://[^"\' ]+|www.[^"\' ]+|http://[^"\' ]+|\w+|\@\w+|\#\w+)'

    dict_ = {}

    for t in tweets:

        tweet = str(t.text, 'utf-8')

        try:
            tweet = normalize('NFKD', tweet.lower()).encode('ASCII', 'ignore')
        except UnicodeEncodeError:
            tweet = normalize('NFKD', tweet.lower().decode('utf-8')).encode('ASCII', 'ignore')

        if isinstance(tweet, str) == False:
            tweet = tweet.decode('utf-8')


        local_patterns = regexp_tokenize(tweet.lower(), pattern)

        hashtags = [e for e in local_patterns if e == side_a or e == side_b]
        
        
        str_date = str(t.date).split(" ")[0] + " " + str(t.date).split(" ")[1].split(":")[0] + ":00"
        
        

        if str_date in dict_.keys():
            dict_[str_date] += hashtags
        else:
            dict_[str_date] = hashtags

    

    for d in sorted(dict_):
        dict_[d] = [w for w in dict_[d] if w in [side_a, side_b]]
        dict_counter = Counter(dict_[d])
        

        fmt = '%Y-%m-%d %H:%M'
        new_date = datetime.strptime(d, fmt).replace(tzinfo=pytz.UTC)

        new_data = HashtagsGraph(side_a, dict_counter[side_a], new_date, context_)
        db_session.add(new_data)
        new_data = HashtagsGraph(side_b, dict_counter[side_b], new_date, context_)
        db_session.add(new_data)

        db_session.commit()


def populate_database(bigrams, frequency_hashtags, frequency_terms, frequency_users_rt, frequency_users_cited, trigrams):
    
    for t in frequency_terms:
        
        new_ = Termos(t[0], t[1])

        db_session.add(new_)
    
    db_session.commit()
    
    for t in frequency_users_rt:
        new_ = UsuariosRT(t[0], t[1])

        db_session.add(new_)
    
    db_session.commit()
    
    for t in frequency_users_cited:
        new_ = UsuariosCitados(t[0], t[1])

        db_session.add(new_)

    db_session.commit()
    
    for t in frequency_hashtags:
        new_ = Hashtags(t[0], t[1])

        db_session.add(new_)

    db_session.commit()
    
    for bigram in bigrams:
        text = ' '.join(word for word in bigram)

        new_ = BigramTrigram(text, 0)

        db_session.add(new_)
    
    db_session.commit()
    
    for trigram in trigrams:
        text = ' '.join(word for word in trigram)

        new_ = BigramTrigram(text, 1)

        db_session.add(new_)
    
    db_session.commit()


def clear_tables():

    try:
        num_rows_deleted = db_session.query(HashtagsGraph).delete()
        db_session.commit()
        print("HashtagsGraph: " + str(num_rows_deleted) + " rows deleted.")
    except Exception as e:
        print("ERROR: " + str(e))
        db_session.rollback()

    try:
        num_rows_deleted = db_session.query(BigramTrigram).delete()
        db_session.commit()
        print("BigramTrigram: " + str(num_rows_deleted) + " rows deleted.")
    except Exception as e:
        print("ERROR: " + str(e))
        db_session.rollback()

    try:
        num_rows_deleted = db_session.query(UsuariosRT).delete()
        db_session.commit()
        print("Usuarios: " + str(num_rows_deleted) + " rows deleted.")
    except Exception as e:
        print("ERROR: " + str(e))
        db_session.rollback()

    try:
        num_rows_deleted = db_session.query(Hashtags).delete()
        db_session.commit()
        print("Hashtags: " + str(num_rows_deleted) + " rows deleted.")
    except Exception as e:
        print("ERROR: " + str(e))
        db_session.rollback()

    try:
        num_rows_deleted = db_session.query(UsuariosCitados).delete()
        db_session.commit()
        print("UsuariosCitados: " + str(num_rows_deleted) + " rows deleted.")
    except Exception as e:
        print("ERROR: " + str(e))
        db_session.rollback()

    try:
        num_rows_deleted = db_session.query(Termos).delete()
        db_session.commit()
        print("Termos: " + str(num_rows_deleted) + " rows deleted.")
    except Exception as e:
        print("ERROR: " + str(e))
        db_session.rollback()


if __name__ == "__main__":

    CONTEXT = "eleicoes2018"
    start(context_=CONTEXT)
