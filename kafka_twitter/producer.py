import twitter 
from json import dumps
from kafka import KafkaProducer

cons_key = "insert"
consumer_secret = "insert"
acc_token = "insert"
acc_sec_token = "insert"

api = twitter.Api(consumer_key='fIaCWYCoyKd3tlm0jNVoFMxn6', consumer_secret='TgGTIm2W6V7DmQQQ55qcEZk47cxzaaGzkcZDVpyiGPC927LW6u' , access_token_key='755394958345969664-gdZQQQrTbb2CybZt5rX5unQb4AMZgak' , access_token_secret='Fsw2F87btwuXpmLdsm9kUnxvsHXAHLmPJYOkasXtb7uU6')

#api = twitter.Api(consumer_key= cons_key , consumer_secret=consumer_secret , access_token_key= acc_token , access_token_secret= acc_sec_token)
results = api.GetStreamFilter(locations=["-178.334698, 18.910361, -66.949895, 71.41286","-167.21211, 53.24541, -140.93442, 71.365162"], languages=['en'], filter_level="low")

producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
    value_serializer=lambda m: dumps(m).encode('ascii'))

def get_tweet():
	data = next(results)
	return data

def test_COVID():
	data = get_tweet()
	text = data.get("text")
	if "corona flu" in text.lower() or "covid" in text.lower() or "coronavirus" in text.lower():
		print("yes")
		producer.send('tweet_stream', value=data)
	else:
		print("no")

while True:
	test_COVID()
