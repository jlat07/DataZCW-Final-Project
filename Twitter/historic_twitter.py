import twitter
import pymysql
from kafka import KafkaConsumer, TopicPartition
from json import loads
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker
import re
import sys
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
import nltk
from datetime import timedelta
from datetime import datetime
from datetime import date
analyser = SentimentIntensityAnalyzer()
stop_words = list(set(stopwords.words('english')))
nltk.download('stopwords')
nltk.download('punkt')

days_back = 30
today = date.today()
start_day = today - timedelta(days_back)

api = twitter.Api(consumer_key='fIaCWYCoyKd3tlm0jNVoFMxn6', consumer_secret='TgGTIm2W6V7DmQQQ55qcEZk47cxzaaGzkcZDVpyiGPC927LW6u' , access_token_key='755394958345969664-gdZQQQrTbb2CybZt5rX5unQb4AMZgak' , access_token_secret='Fsw2F87btwuXpmLdsm9kUnxvsHXAHLmPJYOkasXtb7uU6')
engine = create_engine('mysql+pymysql://root:zipcoder@localhost/twitter')

Base = declarative_base()
class Tweets(Base):
	__tablename__ = 'sentiments'
	tweet_id = Column(Integer, primary_key=True, nullable=False)
	name = Column(String(250))
	text = Column(String(250))
	location = Column(String(250))
	bounding = Column(String(300))
	time_stamp  = Column(Integer)
	state = Column(String(300))
	sentiment = Column(String(50))
	score = Column(String(50))

states = {
	'AK': 'Alaska',
	'AL': 'Alabama',
	'AR': 'Arkansas',
	'AS': 'American Samoa',
	'AZ': 'Arizona',
	'CA': 'California',
	'CO': 'Colorado',
	'CT': 'Connecticut',
	'DC': 'District of Columbia',
	'DE': 'Delaware',
	'FL': 'Florida',
	'GA': 'Georgia',
	'GU': 'Guam',
	'HI': 'Hawaii',
	'IA': 'Iowa',
	'ID': 'Idaho',
	'IL': 'Illinois',
	'IN': 'Indiana',
	'KS': 'Kansas',
	'KY': 'Kentucky',
	'LA': 'Louisiana',
	'MA': 'Massachusetts',
	'MD': 'Maryland',
	'ME': 'Maine',
	'MI': 'Michigan',
	'MN': 'Minnesota',
	'MO': 'Missouri',
	'MP': 'Northern Mariana Islands',
	'MS': 'Mississippi',
	'MT': 'Montana',
	'NA': 'National',
	'NC': 'North Carolina',
	'ND': 'North Dakota',
	'NE': 'Nebraska',
	'NH': 'New Hampshire',
	'NJ': 'New Jersey',
	'NM': 'New Mexico',
	'NV': 'Nevada',
	'NY': 'New York',
	'OH': 'Ohio',
	'OK': 'Oklahoma',
	'OR': 'Oregon',
	'PA': 'Pennsylvania',
	'PR': 'Puerto Rico',
	'RI': 'Rhode Island',
	'SC': 'South Carolina',
	'SD': 'South Dakota',
	'TN': 'Tennessee',
	'TX': 'Texas',
	'UT': 'Utah',
	'VA': 'Virginia',
	'VI': 'Virgin Islands',
	'VT': 'Vermont',
	'WA': 'Washington',
	'WI': 'Wisconsin',
	'WV': 'West Virginia',
	'WY': 'Wyoming'
}


def get_state(loc_name):
	locs = loc_name.split(",")
	if len(locs) > 1:
		if "USA" == locs[1].strip():
			return locs[0]
		elif locs[1].strip() in states.keys(): 
			return states.get(locs[1].strip())

def add_sentiment(tweet):
	tweet = re.sub(r'[^\w\s]', '', tweet)
	words = word_tokenize(tweet, "english", True)
	filtered = [w for w in words if not w in stop_words]
	score = analyser.polarity_scores(" ".join(filtered))
	if 0.0 < score['compound'] <= 1.0:
		return 'Positive'
	elif 0.0 > score['compound'] >= -1.0:
		return 'Negative'
	elif score['compound'] == 0.0:
		return 'Neutral'

def add_score(tweet):
	tweet = re.sub(r'[^\w\s]', '', tweet)
	words = word_tokenize(tweet, "english", True)
	filtered = [w for w in words if not w in stop_words]
	score = analyser.polarity_scores(" ".join(filtered))
	return (score['compound'])

def get_historic_tweets():
	days_back = 30
	today = date.today()
	start_day = today - timedelta(days_back)
	for x in range(days_back):
		results = api.GetSearch(term="coronavirus", since=start_day.isoformat(), count=100, lang=['en'], return_json=True)
		results = results.get("statuses")
		for x in range(100):
			tweet = results[x]
			tweet_id = tweet.get("id")
			name = tweet.get("user").get("name")
			text = tweet.get("text")
			time_stamp = tweet.get("timestamp_ms")
			sentiment = add_sentiment(tweet.get('text'))
			score = add_score(tweet.get('text'))
			if tweet.get("place") == None:
				location = "N/A"
				bounding = "N/A"
				state = "N/A"
			else:
				place = tweet.get("place")
				location = place.get("full_name")
				bounding = str(place.get("bounding_box").get("coordinates"))
				state = full_name = get_state(tweet.get("place").get("full_name"))
			message_sql = Tweets(tweet_id=tweet_id, name=name, text=text, location = location, bounding= bounding, time_stamp = time_stamp, state = state, sentiment = sentiment, score = score)
			Session = sessionmaker(bind=engine)
			session = Session()
			session.add(message_sql)
			session.commit()
		start_day = start_day + timedelta(1)

get_historic_tweets()

