import sys
import os
import pytz

from collections import Counter
from nltk.tokenize import regexp_tokenize
from datetime import datetime

from .d2l_collector.collecting import Collecting
from .d2l_processing.processing import Processing
from db.models import AllTweets, UsuariosCitados, Usuarios, Hashtags, HashtagsGraph, Termos, BigramTrigram
from db.database import db_session

from db.models import AllTweets, UsuariosCitados, Usuarios, Hashtags, HashtagsGraph, Termos, BigramTrigram


collector = Collecting()
processor = Processing()


def start(context_, collect_=False, query_=None):

    waiting_time = 5
    count_tweets = 10
    number_of_attempts = 2
    

    if collect_ and not query_:
        print("Collecting Tweets ...")
        collector.collect(query_, waiting_time, count_tweets, number_of_attempts, context_)

    print("Processing Tweets ...")
    list_texts, list_user = collector.get_tweets_from_database(context_)
    final_words = processor.get_final_words(list_texts, False)
    frequency_terms = processor.get_frequence_terms(final_words)
    frequency_users = processor.get_frequence_users(list_user)
    frequency_users_cited = processor.get_frequence_users_cited()
    frequency_hashtags = processor.get_frequence_hashtags()
    bigrams, trigrams = processor.get_bigrams_trigrams(final_words)

    # Clearing Tables
    print("Cleaning database")
    clear_tables()

     # Insert in database
    print("Populating database")
    populate_database(bigrams, frequency_hashtags, frequency_terms, frequency_users, frequency_users_cited, trigrams)

    #Hashtags Graph
    print("Generating Hashtag count by date")
    hashtag_graph(context_)


def hashtag_graph(context_):

    tweets = AllTweets.query.filter_by(context=context_).all()

    pattern = r'(https://[^"\' ]+|www.[^"\' ]+|http://[^"\' ]+|\w+|\@\w+|\#\w+)'

    dict = {}

    for t in tweets:
        local_patterns = regexp_tokenize(t.text.lower(), pattern)

        hashtags = [e for e in local_patterns if e[0] == '#']

        str_date = str(t.date).split(" ")[0]

        if str_date in dict.keys():
            dict[str_date] += hashtags
        else:
            dict[str_date] = hashtags

    for d in sorted(dict):
        dict[d] = [w for w in dict[d] if w in ['#teamsuperman', '#teambatman']]
        dict_counter = Counter(dict[d])

        fmt = '%Y-%m-%d'
        new_date = datetime.strptime(d, fmt).replace(tzinfo=pytz.UTC)

        new_data = HashtagsGraph('#teamsuperman', dict_counter['#teamsuperman'], new_date, context_)
        db_session.add(new_data)
        new_data = HashtagsGraph('#teambatman', dict_counter['#teambatman'], new_date, context_)
        db_session.add(new_data)

        db_session.commit()


def populate_database(bigrams, frequency_hashtags, frequency_terms, frequency_users, frequency_users_cited, trigrams):
    
    for t in frequency_terms:
        new_ = Termos(t[0], t[1])

        db_session.add(new_)
    
    db_session.commit()
    
    for t in frequency_users:
        new_ = Usuarios(t[0], t[1])

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
        num_rows_deleted = db_session.query(Usuarios).delete()
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

    context = 'bvs'
    start(context)
