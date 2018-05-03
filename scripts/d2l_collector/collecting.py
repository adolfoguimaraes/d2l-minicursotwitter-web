#coding=utf-8

from twython import Twython

from .twittercollector import TwitterCollector

from db.models import AllTweets
from db.database import  db_session

class Collecting():

    def __init__(self):

        self.tc = TwitterCollector()


    def collect(self, query_search, waiting_time, count, number_of_attempts, context):

        tweets = self.tc.collect(query_search, waiting_time, count, number_of_attempts)

        for t in tweets:
            if 'text' in t.keys():
                value = {
                    'tweet_id': t['id'],
                    'user': t['user']['screen_name'],
                    'text': t['text'],
                    'date': t['posted_at'],
                    'user_image': t['user']['profile_image_url'],
                    'context': context
                }

                new_ = Tweets(value['tweet_id'], value['user'], value['text'], value['date'], value['user_image'], value['context'])

                db_session.add(new_)
                db_session.commit()



    # Ler tweets já gravados no banco de dados e retorna uma lista com os textos e com os usuários
    def get_tweets_from_database(self, context):

        tweets = AllTweets.query.filter_by(context=context).all()

        list_text = []
        list_user = []

        for tweet in tweets:
            list_text.append(tweet.text)
            list_user.append(tweet.user)


        return list_text, list_user