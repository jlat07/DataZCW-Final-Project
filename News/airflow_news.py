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
news_api_key = 'e5c1081b366a416caa370c85bb04d392'
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

def add_sentiment(news):
    news = re.sub(r'[^\w\s]', '', news)
    words = word_tokenize(news, "english", True)
    filtered = [w for w in words if not w in stop_words]
    score = analyser.polarity_scores(" ".join(filtered))
    if 0.0 < score['compound'] <= 1.0:
        return 'Positive'
    elif 0.0 > score['compound'] >= -1.0:
        return 'Negative'
    elif score['compound'] == 0.0:
        return 'Neutral'

def add_score(tweets):
    tweet = re.sub(r'[^\w\s]', '', tweets)
    words = word_tokenize(tweet, "english", True)
    filtered = [w for w in words if not w in stop_words]
    score = analyser.polarity_scores(" ".join(filtered))
    return (score['compound'])


def get_numbers():
	now = datetime.now()-timedelta(12)
	start_date = datetime.now()-timedelta(hours=13)
	all_articles = newsapi.get_everything(q='covid-19', 
		from_param=start_date.isoformat()[0:19], 
		to=now.isoformat()[0:19],
		language='en',
		sort_by='relevancy', 
		page=1,
		page_size=100) 
	for x in range(len(all_articles.get("articles"))):
		article = all_articles.get("articles")[x]
		if article.get("content") != None:
			author = str(article.get('author'))
			title = str(article.get('title'))
			content = str(article.get('content'))
			published_date = str(article.get('publishedAt'))
			sentiment = str(add_sentiment(content))
			score = str(add_score(content))
			aut_title = str(published_date + title)
			message_sql = articles(author=author, title=title, content=content, date=published_date, sentiment = sentiment, score= score,  unique_identify = aut_title)
			Session = sessionmaker(bind=engine)
			session = Session()
			session.add(message_sql)
			session.commit()

get_numbers()