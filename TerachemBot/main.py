#!/usr/bin/env python

import tweepy
import logging
from config import create_api
import time
from comp import compute

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

def check_mentions(api, keywords, since_id):
    logger.info("Retrieving mentions")
    new_since_id = since_id
    for tweet in tweepy.Cursor(api.mentions_timeline,
        since_id=since_id).items():
        new_since_id = max(tweet.id, new_since_id)
        if tweet.in_reply_to_status_id is not None:
            continue
        if any(keyword in tweet.text.lower() for keyword in keywords):
            print('message',tweet.text.lower())
            print('user',tweet.user.screen_name)
            logger.info(f"Answering to {tweet.user.name}")

            pro = tweet.text.lower().split()[2]
            molecule = tweet.text.lower().split()[3]
            functional = tweet.text.lower().split()[4]

            print(pro,molecule,functional)
            output = compute(pro,molecule,'gas',functional)  # setup and launch calculation

            print('output TCC:',output)
            text = '@'+tweet.user.screen_name+'  ' + output 
            print('text:',text)
            api.update_status(
                status=text,
                in_reply_to_status_id=tweet.id,
            )
    return new_since_id

def main():
    api = create_api()  # Twitter authentication
    since_id = 1
    while True:
        since_id = check_mentions(api, ["compute", "calculate"], since_id)   # check mentions
        logger.info("Waiting...")
        time.sleep(30)

if __name__ == "__main__":
    main()
