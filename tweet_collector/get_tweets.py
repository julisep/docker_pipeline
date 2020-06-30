import config
from tweepy import OAuthHandler, Stream
from tweepy.streaming import StreamListener
import json
import logging
import pprint
from sqlalchemy import create_engine
from pymongo import MongoClient

def authenticate():
    """Function for handling Twitter Authentication. Please note
       that this script assumes you have a file called config.py
       which stores the 4 required authentication tokens:

       1. CONSUMER_API_KEY
       2. CONSUMER_API_SECRET
       3. ACCESS_TOKEN
       4. ACCESS_TOKEN_SECRET

    See course material for instructions on getting your own Twitter credentials.
    """
    auth = OAuthHandler(config.CONSUMER_API_KEY, config.CONSUMER_API_SECRET)
    auth.set_access_token(config.ACCESS_TOKEN, config.ACCESS_TOKEN_SECRET)

    return auth

class TwitterListener(StreamListener):

    def on_data(self, data):

        """Whatever we put in this method defines what is done with
        every single tweet as it is intercepted in real-time"""

        t = json.loads(data) #t is just a regular python dictionary.

        text = t['text']
        if 'extended_tweet' in t:
            text =  t['extended_tweet']['full_text']
        if 'retweeted_status' in t:
            r = t['retweeted_status']
            if 'extended_tweet' in r:
                text =  r['extended_tweet']['full_text']

        tweet = {
        'text': text,
        'username': t['user']['screen_name'],
        'followers_count': t['user']['followers_count']
        }

        logging.warning('INCOMING TWEET!')
        tweets.insert(tweet)
        logging.warning('SUCCESSFULLY ADDED TO DB!')


    def on_error(self, status):
        if status == 420:
            print(status)
            return False

# Connection to mongoDb
client = MongoClient(host='mongo_db', port=27017)
# host mongo_db indicates that we are talking directly to the container mongo_db
# of the docker-compose pipeline
db = client.twitter_data
tweets = db.tweets

# Connection to Postgres
#engine = create_engine('postgres://postgres:xxxx@my_database:5432/postgres')
# user:password@host:port/my_database
# for host insert name of the service defined in docker-compose.yaml
# user and password are also defined in docker-compose.yaml
# for port, insert internal port of the container as defined in docker-compose.yaml
# default database in postgres is called 'postgres'
# create_query = """
# CREATE TABLE IF NOT EXISTS tweets (
# user_name TEXT,
# tweet_text TEXT
# );
# """
#engine.execute(create_query)

if __name__ == '__main__':

    auth = authenticate()
    listener = TwitterListener()
    stream = Stream(auth, listener)
    stream.filter(track=['ikea'], languages=['en'])