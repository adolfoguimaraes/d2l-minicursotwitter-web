from datetime import datetime
import pytz
import time


class Twitter():

    def __init__(self):

        self.consumer_key = "EhjkX3eL1KN2pitOt4PRRDuuo" # Get Keys and Access Token at apps.twitter.com
        self.consumer_secret = "MCfsfrFD2NFC7vCxYon41ukxOuCSAvauskmxIA4aCW7P9txKV1" # Get Keys and Access Token at apps.twitter.com
        self.access_token = "736392442384154624-YjF2w3SVj4wXKV2qWYgQKQsHBDz1CSz" # Get Keys and Access Token at apps.twitter.com
        self.access_token_secret = "hJiihk0r7efTOoCjCX0qbMW0zl298LumPpC69jAgvZubm" # Get Keys and Access Token at apps.twitter.com


        self.credentials = {
            'consumer_key': self.consumer_key,
            'consumer_secret': self.consumer_secret,
            'access_token': self.access_token,
            'access_token_secret': self.access_token_secret
        }

    def get_credentials(self):
        return self.credentials

    def get_tweet_data(self, data):

        # Id do twitter
        object_id = data['id']

        # Id do usuário que postou o texto
        user_id = data['user']['id']

        # Usuário que postou o texto
        user_name = data['user']['screen_name']

        # Texto postado em utf-8
        if 'retweeted_status' in data.keys():    
            if data['retweeted_status']['truncated'] == False:
                text = data['retweeted_status']['text'].encode('utf-8')
            else:
                if 'extended_tweet' in data['retweeted_status'].keys():
                    text = data['retweeted_status']['extended_tweet']['full_text'].encode('utf-8')
                else:
                    text = data['retweeted_status']['text'].encode('utf-8')
            rt_user = data['retweeted_status']['user']['screen_name']
        else:
            if data['truncated'] == False:
                text = data['text'].encode('utf-8')
            else:
                if 'extended_tweet' in data.keys():
                    text = data['extended_tweet']['full_text'].encode('utf-8')
                else:
                    text = data['text'].encode('utf-8')
            rt_user = ""


        # Data que foi publicado
        posted_at_tweet = data['created_at']

        # Data que foi publicado formatada
        fmt = '%Y-%m-%d %H:%M:%S.%f'
        new_date = datetime.strptime(posted_at_tweet, '%a %b %d %H:%M:%S +0000 %Y').replace(tzinfo=pytz.UTC)

        published_date = str(new_date.strftime(fmt))

        tweet = {
            'object_id': object_id,
            'user_id': user_id,
            'user_name': user_name,
            'text': text,
            'user_rt': rt_user,
            'date_formated': new_date,
            'date_str': published_date 
        }

        return tweet