'''Module that tells python jokes'''

import slack
from sqlalchemy import create_engine
from config import OAUTH_TOKEN

# Connectionto slack client
client = slack.WebClient(token=OAUTH_TOKEN)

# Connection to Postgres
engine = create_engine('postgres://postgres:xxxx@postgres_db:5432/postgres')

happiest_tweet_query = """
SELECT * FROM tweets
ORDER BY sentiment_score DESC
LIMIT 1;
"""

happiest_tweet = engine.execute(happiest_tweet_query).fetchall()
#print(happiest_tweet)
#print(type(happiest_tweet))

tweet_slack = f"""Happiest tweet:
User {happiest_tweet[0][0]} posted:

{happiest_tweet[0][1]}

The tweet received a Sentinent Score of {happiest_tweet[0][2]}.
"""

#print(tweet_slack)

response = client.chat_postMessage(channel='#random', text=tweet_slack)
