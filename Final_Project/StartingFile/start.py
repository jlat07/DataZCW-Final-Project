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
from newsapi import NewsApiClient
from dotenv import load_dotenv
import os
from email.utils import parsedate_tz
load_dotenv()
consumer_key=os.getenv("consumer_key")
consumer_secret = os.getenv("consumer_secret") 
access_token_key = os.getenv("access_token_key") 
access_token_secret = os.getenv("access_token_secret") 
news_api_key = os.getenv("NEWS_API_KEY")
newsapi = NewsApiClient(api_key = news_api_key)
analyser = SentimentIntensityAnalyzer()
stop_words = list(set(stopwords.words('english')))
nltk.download('stopwords')
nltk.download('punkt')


api = twitter.Api(consumer_key=consumer_key, consumer_secret=consumer_secret , access_token_key=access_token_key , access_token_secret=access_token_secret)
engine = create_engine('mysql+pymysql://root:zipcoder@localhost/twitter')

Base = declarative_base()
class Tweets(Base):
	__tablename__ = 'sentiments'
	tweet_id = Column(Integer, primary_key=True, nullable=False)
	name = Column(String(500))
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


def to_timestamp(datestring):
	time_tuple = parsedate_tz(datestring.strip())
	dt = datetime(*time_tuple[:6])
	date_time = dt - timedelta(seconds=time_tuple[-1])
	timestamp = int(datetime.timestamp(date_time))*1000
	return timestamp

def get_historic_tweets():
	days_back = 9
	today = datetime.today()
	since = today - timedelta(days_back -1)
	until =today - timedelta(days_back -2)
	total = 0
	for x in range(days_back):
		results = api.GetSearch(term="Coronavirus", until=until.isoformat(), since=since.isoformat(), count=100, lang=['en'], return_json=True)
		results = results.get("statuses")
		total += len(results)
		for x in range(len(results)):
			tweet = results[x]
			tweet_id = tweet.get("id")
			name = tweet.get("user").get("name")
			text = tweet.get("text")
			time_stamp = to_timestamp(tweet.get("created_at"))
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
		since = since + timedelta(1)
		until = until + timedelta(1)

get_historic_tweets()

engine2 = create_engine('mysql+pymysql://root:zipcoder@localhost/News')

class articles(Base):
    __tablename__ = 'news'
    author = Column(String(4294967294))
    title = Column(String(500))
    content = Column(String(4294967294))
    date  = Column(Integer)
    sentiment = Column(String(50))
    score = Column(String(50))
    unique_identify = Column(String(4294967294), primary_key = True)

def get_historic_news():
	today = date.today()
	start_date = today - timedelta(8)
	next_day = start_date + timedelta(1)
	while start_date != (today+timedelta(1)):
		all_articles = newsapi.get_everything(q='covid-19', 
			from_param=start_date.isoformat(), 
			to=start_date.isoformat(),
			language='en',
			sort_by='relevancy', 
			page=1,
			page_size=100) 
		for x in range(len(all_articles.get("articles"))):
			article = all_articles.get("articles")[x]
			if article.get("content") != None:
				title = str(article.get('title'))
				content = str(article.get('content'))
				published_date = str(article.get('publishedAt'))
				published_date = datetime.strptime(published_date,"%Y-%m-%dT%H:%M:%SZ")
				published_date = datetime.timestamp(published_date)*1000
				author = str(article.get('author'))
				sentiment = str(add_sentiment(content))
				score = str(add_score(content))
				aut_title = str(str(author)+ " " + str(title))
				message_sql = articles(author=author, title=title, content=content, date=published_date, sentiment = sentiment, score= score,  unique_identify = aut_title)
				Session = sessionmaker(bind=engine2)
				session = Session()
				session.add(message_sql)
				session.commit()
		start_date = start_date + timedelta(1)


get_historic_news()