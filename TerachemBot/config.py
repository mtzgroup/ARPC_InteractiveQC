# tweepy-bots/bots/config.py
import tweepy
import logging
import os

logger = logging.getLogger()

def create_api():
   
    # Twitter credentials: TO ADD
    consumer_key =         # TO ADD 
    consumer_secret =      # TO ADD
    access_token =         # TO ADD
    access_token_secret =  # TO ADD

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth) 
    try:
        api.verify_credentials()
    except Exception as e:
        logger.error("Error creating API", exc_info=True)
        raise e
    logger.info("API created")
    return api


