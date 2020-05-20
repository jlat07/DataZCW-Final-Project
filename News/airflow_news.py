from datetime import timedelta
from datetime import datetime
from datetime import date
import sqlalchemy
from sqlalchemy import create_engine
import pymysql
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker
import requests
import os
from newsapi import NewsApiClient
import re
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
import nltk
from newsapi import NewsApiClient
analyser = SentimentIntensityAnalyzer()
stop_words = list(set(stopwords.words('english')))
nltk.download('stopwords')
nltk.download('punkt')
today = date.today()
today = today.isoformat()
news_api_key = 'INSERT_HERE'
newsapi = NewsApiClient(api_key = news_api_key)

engine = create_engine('mysql+pymysql://root:zipcoder@localhost/News')


Base = declarative_base()
class articles(Base):
    __tablename__ = 'news'
    author = Column(String(250))
    title = Column(String(500))
    content = Column(String(4294967294))
    date  = Column(Integer)
    sentiment = Column(String(50))
    score = Column(String(50))
    unique_identify = Column(String(200), primary_key = True)

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


def get_numbers():
	today = date.today()
	start_date = today
	page = 1
	all_articles = newsapi.get_everything(q='covid-19',
		sources='abc-news', 
		from_param=today.isoformat(), 
		to=today.isoformat(),
		language='en',
		sort_by='relevancy', 
		page=page)
	number_results = all_articles.get('totalResults')
	number_of_full_pages = (number_results//20)
	number_left_overs = number_results%20
	for x in range(number_of_full_pages):
		all_articles = newsapi.get_everything(q='covid-19',
		sources='abc-news', 
		from_param=start_date, 
		to=start_date,
		language='en',
		sort_by='relevancy', 
		page= x+1)
		for x in range(20):
			article = all_articles.get("articles")[x]
			author = article.get('author')
			title = article.get('title')
			content = article.get('content')
			published_date = article.get('publishedAt')
			sentiment = add_sentiment(content)
			score = add_score(content)
			aut_title = str(published_date + title)
			message_sql = articles(author=author, title = title, content=content, date=published_date, sentiment = sentiment, score= score,  unique_identify = aut_title)
			Session = sessionmaker(bind=engine)
			session = Session()
			session.add(message_sql)
			session.commit()
	leftover_articles = newsapi.get_everything(q='covid-19',
		sources='abc-news', 
		from_param=start_date, 
		to=start_date,
		language='en',
		sort_by='relevancy', 
		page=number_of_full_pages+1)
	for i in range(number_left_overs):
		article = leftover_articles.get("articles")[i]
		author = article.get('author')
		title = article.get('title')
		content = article.get('content')
		published_date = article.get('publishedAt')
		sentiment = add_sentiment(content)
		score = add_score(content)
		aut_title = str(published_date + title)
		message_sql = articles(author=author, title = title, content=content, date=published_date, sentiment = sentiment, score= score,  unique_identify = aut_title)
		Session = sessionmaker(bind=engine)
		session = Session()
		session.add(message_sql)
		session.commit()

get_numbers()