# Dockerized sentiment analysis of a Twitter stream
-- Week 7 of the SPICED DataScience Bootcamp --

A docker-compose pipeline is built with the following tasks:
- 1 Collect tweets with certain keywords via Twitter's API
- 2 Store text, username and follower count in a mongoDB
- 3 Read the information from the mongoDB, perform Sentiment Analysis
- 4 Store result in a Postgres database
- 5 Create a slack bot

To run this pipeline access to the Twitter API is required.Please note that this script assumes you have a file called <config.py>
which stores the 4 required authentication tokens located in the folder <tweet_collector/>:
       1. CONSUMER_API_KEY
       2. CONSUMER_API_SECRET
       3. ACCESS_TOKEN
       4. ACCESS_TOKEN_SECRET
