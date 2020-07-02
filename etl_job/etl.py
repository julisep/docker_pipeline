'''Extract Transform Load process for the pipeline project'''

'''
We will extract tweets from MongoDB, transform the JSON like objects into entries for relational database tables and we perform sentiment analysis on the tweets (the sentiment analysis is part of the transform), then load the transformed data into postgres.

1. Extract data from MongoDB
    - Connect to database
    - Write query to extract the data

2. Perform sentiment analysis/transform
    - Must be included in the afternoon

3. Load transformed data into Postgres
    - Connect to the Postgres database server
    - Create a table
    - Write into that table
'''

import logging
import time
from datetime import datetime
from pymongo import MongoClient
from sqlalchemy import create_engine
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer




def extract(last_timestamp):
    '''Extracts all tweets from the MongoDB database'''
    extracted_tweets = list(tweets_mongo.find({"timestamp" : {"$gt" : last_timestamp}}))
    logging.critical(f'EXTRACTED {len(extracted_tweets)} TWEETS FROM MONGO DB')
    logging.critical(f'LAST TIMESTAMP {last_timestamp}')
    return extracted_tweets

def transform(extracted_tweets):
    '''
    Performs sentiment analysis on the tweets and returns it in a format so the tweets can be written into a Postgres database
    '''
    transformed_tweets = []
    for tweet in extracted_tweets:
        # tweet is a dictionary
        sentiment = s.polarity_scores(tweet['text'])
        tweet['sentiment_score'] = sentiment['compound']
        transformed_tweets.append(tweet)
    return transformed_tweets

def load(transformed_tweets):
    ''' Load transformed data into the postgres database'''
    for tweet in transformed_tweets:
        insert_query = "INSERT INTO tweets VALUES (%s, %s, %s);"
        data = [tweet["name"], tweet["text"], tweet["sentiment_score"]]
        engine.execute(insert_query, data)
    logging.critical(f'ADDED {len(transformed_tweets)} TRANSFORMED TWEETS TO POSTGRES DB')

def try_times(func, max_tries, sleep_time):
    '''Tries to call a function a number of times.
        func = function that returns object
        max_tries = maximum number of attempts
        sleep_time = time to wait until next attempt
    '''
    for i in range(max_tries):
        try:
            return func()
        except:
            time.sleep(sleep_time)
    raise Exception("Maximum tries exceded.")

# Wait for databases to be ready
time.sleep(10)
# Connection to MongoDB
client = MongoClient(host='mongo_db', port=27017)
db = client.twitter_data # access database
tweets_mongo = db.tweets # access collection

# Connection to Postgres
engine = create_engine('postgres://postgres:xxxx@postgres_db:5432/postgres')

# Instantiate Sentiment Analyzer
s = SentimentIntensityAnalyzer()

# Create table in postgres database if it doesn't exist yet
create_query = """
CREATE TABLE IF NOT EXISTS tweets (
name TEXT,
text TEXT,
sentiment_score REAL
);
"""
engine.execute(create_query)

# Instantiate last timestamp
last_timestamp = datetime.strptime('1970-01-01 00:00:00', '%Y-%m-%d %H:%M:%S')

# Until we stop the container or an error returns, do all the stuff
while True:
    extracted_tweets = extract(last_timestamp)
    if len(extracted_tweets) != 0:
        transformed_tweets = transform(extracted_tweets)
        load(transformed_tweets)
        last_timestamp = extracted_tweets[-1]['timestamp']
    time.sleep(60)
