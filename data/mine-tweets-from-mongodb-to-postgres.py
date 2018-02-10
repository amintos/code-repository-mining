#!/usr/bin/env python3

# this script should be run AFTER the tweets have been crawled and
# thus a TweetScraper collection exists in MongoDB
# LEGACY - since TweetScraper has PostgreSQL saving capability it should not be needed anymore

import config
import psycopg2
from pymongo import MongoClient

# set up PostgreSQL connection
dropViewStatement1   = "DROP MATERIALIZED VIEW IF EXISTS  view_cve_referring_tweets_extracted_cves;"
dropViewStatement2   = "DROP MATERIALIZED VIEW IF EXISTS  view_cve_referring_tweets_extracted_links;"
dropTableStatement   = "DROP TABLE IF EXISTS cve_referring_tweets;"
createTableStatement ="""
CREATE TABLE cve_referring_tweets(
  id BIGINT PRIMARY KEY,
  user_id BIGINT,
  username VARCHAR(15),
  text VARCHAR(2048),
  is_reply BOOLEAN,
  is_retweet BOOLEAN,
  reply_count INT,
  favorite_count INT,
  retweet_count INT,
  timestamp TIMESTAM2
);
"""
createViewStatement1 = """
CREATE MATERIALIZED VIEW view_cve_referring_tweets_extracted_cves AS
SELECT
  id AS tweet_id,
  regexp_matches(text, 'CVE-[0-9]{3,4}-[0-9]{3,7}', 'g') as cve
FROM cve_referring_tweets
WITH DATA;
"""
createViewStatement2 = """
CREATE MATERIALIZED VIEW view_cve_referring_tweets_extracted_domains AS
SELECT
  id AS tweet_id,
  regexp_matches(text, 'http[s]:\/\/?\ ?([-a-zA-Z0-9:%._\+~#=]{2,255}\.[a-z]{2,6})', 'g') AS domain
FROM cve_referring_tweets
WITH DATA;
"""
insertTweetStatement = "INSERT INTO cve_referring_tweets VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

postgresConnection = psycopg2.connect(dbname=config.postgresql.dbname,
                                      user=config.postgresql.user,
                                      password=config.postgresql.password)
postgresCursor = postgresConnection.cursor()

# set up MongoDB connection
mongoclient = MongoClient('localhost', 27017)
mongotweets = mongoclient['TweetScraper']['tweet']

# create clean table setup
postgresCursor.execute(dropTableStatement)
postgresCursor.execute(createTableStatement)
postgresCursor.execute(dropViewStatement1)
postgresCursor.execute(dropViewStatement2)

# insert every tweet into postgres
for tweet in mongotweets.find():
    postgresCursor.execute(insertTweetStatement, (
        tweet['ID'],
        tweet['user_id'],
        tweet['usernameTweet'],
        tweet['text'],
        tweet['is_reply'],
        tweet['is_retweet'],
        tweet['nbr_reply'],
        tweet['nbr_favorite'],
        tweet['nbr_retweet'],
        tweet['datetime']
    ))

#postgresCursor.execute(createViewStatement1);
#postgresCursor.execute(createViewStatement2);

postgresConnection.commit()
postgresCursor.close()
postgresConnection.close()
