from __future__ import unicode_literals
import sys
import tweepy
import os
import json
import pandas as pd
from sqlalchemy import create_engine
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener
import json
import re
import dateparser
from datetime import datetime, timedelta, timezone

import pykafka


class TweetListner(StreamListener):

    def __init__(self, kafkaProducer):
        print("Tweet producer Intialized")
        self.producer = kafkaProducer
        self.engine = create_engine('mysql+pymysql://root:zipcoder@localhost/twitter')

    def on_data(self, data):
        """"
        Called when raw data is receive from connection. Return False to stop stream and close connection.
        """
        try:
            # parse into JSON
            # print(json.dumps(data))
            json_data = json.loads(data)
            print(json_data)
            tweet = json_data["text"]
            tweet = re.sub(r',', ' ', tweet)
            place = json_data['place']
            location = "N/A"
            if place is not None:
                location = place['full_name']
                if place['place_type'] == "city":
                    location = location.split(",")[1]
                elif place['place_type'] == "admin":
                    location = location.split(",")[0]
            location = re.sub(r',', ' ', location)
            print(str(location) + "\n")
            timestamp = ''
            if json_data['created_at'] is not None:
                timestamp = json_data['created_at']
            self.producer.produce(bytes(json.dumps(str(tweet) + "," + str(location) +
                                                   "," + str(timestamp)).encode('utf-8')))
        except KeyError as e:
            print("Error in data")

        return True

    def on_error(self, status_code):
        """Called when a new status arrives"""
        print(status_code)
        return True


def connect_to_twitter(kafkaProducer, tracks):
    twitterApiKey = ""
    twitterApiSecret = ''
    twitterApiToken = ''
    twitterApiTokenSecret = ''

    auth = OAuthHandler(twitterApiKey, twitterApiSecret)
    auth.set_access_token(twitterApiToken, twitterApiTokenSecret)

    tweet_stream = Stream(auth, TweetListner(kafkaProducer))
    tweet_stream.filter(track=tracks, languages=["en"], locations=[-178.334698, 18.910361, -66.949895, 71.41286,
                                                                   -167.21211, 53.24541, -140.93442, 71.365162])


if __name__ == "__main__":
    host = 'localhost'
    port = '9092'
    topic = 'tweet_stream'
    tracks = ["corona flu", "covid", "coronavirus"]

    kafkaClient = pykafka.KafkaClient(host + ":" + port)
    kafkaProducer = kafkaClient.topics[bytes(topic, 'utf-8')].get_producer()
    connect_to_twitter(kafkaProducer, tracks)
