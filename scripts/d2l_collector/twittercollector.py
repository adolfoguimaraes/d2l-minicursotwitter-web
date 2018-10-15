import time
import pytz
import sys

from sqlalchemy import exc

from db.models import AllTweets
from db.database import db_session


from datetime import datetime
from twython import Twython
from scripts.d2l_collector.twitter import Twitter

class TwitterCollector():

    def __init__(self):

        self.twitter = Twitter()
        self.credentials = self.twitter.get_credentials()
        self.twython = Twython(self.credentials['consumer_key'], self.credentials['consumer_secret'], self.credentials['access_token'], self.credentials['access_token_secret'])


    def collect(self, query, context, waiting_time, count, number_of_attempts):

        

        if query == '':
            return

        last_since = -1

        tweets_collect = []
        list_ids = []

        for i in range(0, number_of_attempts):

            print("Collecting " + query + "... Attempt: " + str(i))

            if i == 0:
                results = self.twython.search(q=query, count=count, lang='pt')
            else:
                results = self.twython.search(q=query, count=count, lang='pt', since_id=last_since)

            count_control = 0

            for t in results['statuses']:
                
                tweet = self.twitter.get_tweet_data(t)

                if count_control == 0:
                    last_since = tweet['object_id']
                    count_control += 1
                
                try:
                    tweet_instance = AllTweets(tweet['object_id'], tweet['user_name'], tweet['text'], tweet['date_formated'], tweet['user_rt'], tag, context)
                    db_session.add(tweet_instance)
                    db_session.commit()
                    print("Saved " + str(tweet['object_id']))
                except exc.IntegrityError as e:
                    print("The tweet " + str(tweet['object_id']) + " has already on database")
                    db_session.rollback()
                except Exception as e:
                    raise Exception("Database Error: " + str(e))
                
                
            
            #waiting_time in seconds
            print("Waiting Sleep Time ...")
            time.sleep(waiting_time)


        

if __name__ == "__main__": 

    p = sys.argv
     
    if len(p) < 3:
        print("Number of arguments is not correct")
        exit(0)
    elif len(p) == 3:
        tag = str(p[1])
        context = str(p[2])
        language = None
    else:
        tag = str(p[1])
        context = str(p[2])
        language = str(p[3])

    tw = TwitterCollector()
    tw.collect(tag, context, 5, 10, 2)

    
    