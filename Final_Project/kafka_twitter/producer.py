import twitter 
from json import dumps
from kafka import KafkaProducer
from dotenv import load_dotenv
import os
load_dotenv()
cons_key=os.getenv("consumer_key")
consumer_secret = os.getenv("consumer_secret") 
acc_token = os.getenv("access_token_key") 
acc_sec_token = os.getenv("access_token_secret") 
api = twitter.Api(consumer_key= cons_key , consumer_secret=consumer_secret , access_token_key= acc_token , access_token_secret= acc_sec_token)
results = api.GetStreamFilter(track= ("corona flu" , "covid" , "coronavirus" ),locations=["-178.334698, 18.910361, -66.949895, 71.41286","-167.21211, 53.24541, -140.93442, 71.365162"], languages=['en'], filter_level="low")

producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
    value_serializer=lambda m: dumps(m).encode('ascii'))

def get_tweet():
	data = next(results)
	return data

def test_COVID():
	data = get_tweet()
	text = data.get("text")
	try:
		if "corona flu" in text.lower() or "covid" in text.lower() or "coronavirus" in text.lower():
			producer.send('tweet_stream', value=data)
	except AttributeError:
		pass


while True:
	test_COVID()
