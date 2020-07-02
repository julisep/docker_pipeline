import config
from tweepy import OAuthHandler, Stream
from tweepy.streaming import StreamListener
import json
from datetime import datetime
import logging
import time
from pymongo import MongoClient




def authenticate():
    """Function for handling Twitter Authentication. Please note
       that this script assumes you have a file called config.py
       which stores the 4 required authentication tokens:

       1. CONSUMER_API_KEY
       2. CONSUMER_API_SECRET
       3. ACCESS_TOKEN
       4. ACCESS_TOKEN_SECRET

        """
    auth = OAuthHandler(config.CONSUMER_API_KEY, config.CONSUMER_API_SECRET)
    auth.set_access_token(config.ACCESS_TOKEN, config.ACCESS_TOKEN_SECRET)

    return auth

class TwitterListener(StreamListener):

    def on_data(self, data):
        """Whatever we put in this method defines what is done with
        every single tweet as it is intercepted in real-time"""
        t = json.loads(data)
        text = t['text']
        if 'extended_tweet' in t:
            text =  t['extended_tweet']['full_text']
        if 'retweeted_status' in t:
            r = t['retweeted_status']
            if 'extended_tweet' in r:
                text =  r['extended_tweet']['full_text']
        timestamp = datetime.strptime(t['created_at'], '%a %b %d %H:%M:%S +0000 %Y')
        tweet = {
        'text': text,
        'name': t['user']['screen_name'],
        'timestamp': timestamp
        }
        tweets.insert(tweet)
        logging.warning(f'SUCCESSFULLY ADDED TWEET WITH TIMESTAMP {tweet["timestamp"]} TO MONGO DB!')

    def on_error(self, status):
        if status == 420:
            print(status)
            return False

def try_database(func, max_tries, sleep_time):
    '''Tries to call a function a number of times.
        func = function that returns database connection
        max_tries = maximum number of attempts
        sleep_time = time to wait until next attempt
    '''
    for i in range(max_tries):
        logging.critical(f'Try to connect to database number: {i+1}')
        try:
            return func()
        except:
            logging.warning('Failed to access database. Will try again in {sleep_time} s.')
            time.sleep(sleep_time)
    raise Exception("Couldn't connect to database. Maximum tries exceded.")




# Connection to mongoDb
#client = MongoClient(host='mongo_db', port=27017)
client = try_database(lambda: MongoClient(host='mongo_db', port=27017), 5, 10)
db = client.twitter_data
tweets = db.tweets

# Get the tweets
if __name__ == '__main__':
    auth = authenticate()
    listener = TwitterListener()
    stream = Stream(auth, listener)
    stream.filter(track=['berlin'], languages=['en'])
