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
from pymongo import MongoClient
from sqlalchemy import create_engine

# Connection to MongoDB
client = MongoClient(host='mongo_db', port=27017)
db = client.twitter_data # access database
tweets_mongo = db.tweets # access collection

# Connection to Postgres
engine = create_engine('postgres://postgres:xxxx@postgres_db:5432/postgres')
# user:password@host:port/my_database
# for host insert name of the service defined in docker-compose.yaml
# user and password are also defined in docker-compose.yaml
# for port, insert internal port of the container
# default database in postgres is called 'postgres'

def extract():
    '''Extracts all tweets from the MongoDB database'''
    extracted_tweets = list(tweets_mongo.find())
    return extracted_tweets

def transform(extracted_tweets):
    '''
    Performs sentiment analysis on the tweets and returns it in a format so the tweets can be written into a Postgres database
    '''
    transformed_tweets = []
    for tweet in extracted_tweets:
        # tweet is a dictionary
        tweet['sentiment_score'] = 1 # must be calcualted here
        transformed_tweets.append(tweet)
    return transformed_tweets


def load(transformed_tweets):
    ''' Load transformed data into the postgres database'''
    for tweet in transformed_tweets:
        # insert_query = f"""INSERT INTO tweets VALUES ('{tweet['username']}', '{tweet['text']}', '{tweet['sentiment_score']}');"""
        data = [tweet["name"], tweet["text"], tweet["sentiment_score"]]
        insert_query = "INSERT INTO tweets VALUES (%s, %s, %s);"
        engine.execute(insert_query, data)
    logging.critical('SUCCESSFULLY ADDED TRANSFORMED TWEETS TO POSTGRES DB!')

# >>> SQL = "INSERT INTO authors (name) VALUES (%s);" # Note: no quotes
# >>> data = ("O'Reilly", )
# >>> cur.execute(SQL, data) # Note: no % operator

create_query = """
CREATE TABLE IF NOT EXISTS tweets (
name TEXT,
text TEXT,
sentiment_score TEXT
);
"""
engine.execute(create_query)

# Until we stop the container or an error returns, do the stuff
while True:
    extracted_tweets = extract()
    transformed_tweets = transform(extracted_tweets)
    load(transformed_tweets)
    time.sleep(60)

'''
In the code as it is written right now, the whole collection of documents from the MOngoDB is extracted in every single run of the ETL process and is transformed and loaded into the Postgres database.
That means that we will have a lot of duplicates in the Postgres Database.

Easiest fix:
- only load the last tweet

A bit more elaborate fixes:
- Introduce the timestamp into the MongoDB database and onyl query the tweets that have not been extracted in the last run.
- If you run the tweepy, you get a data field called 'created_at' that we could use

- You could tag the extracted tweets in the MongoDB

- You could drop the Postgres Database Table each time
'''
