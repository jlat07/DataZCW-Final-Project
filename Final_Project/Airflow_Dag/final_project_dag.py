#import datadotworld as dw
#import papermill as pm
#from airflow.operators.papermill_operator import PapermillOperator
#from airflow.operators.postgres_operator import PostgresOperator
#from airflow.operators.postgres_operator import PostgresHook
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash_operator import BashOperator
from airflow import DAG
from airflow.utils.dates import days_ago
import airflow.hooks.S3_hook
from airflow.hooks.base_hook import BaseHook
from airflow.providers.mysql.operators.mysql import MySqlOperator
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
from dotenv import load_dotenv
import os
load_dotenv()
analyser = SentimentIntensityAnalyzer()
stop_words = list(set(stopwords.words('english')))
nltk.download('stopwords')
nltk.download('punkt')
today = date.today()
today = today.isoformat()
news_api_key = os.getenv("NEWS_API_KEY")
newsapi = NewsApiClient(api_key = news_api_key)

default_args = {
    'owner': 'James Kocher',
    'depends_on_past': False,
    'start_date': datetime.now(),
    'retries': 0
	}

dag = DAG(
	"Final_Project_Pipeline",
	default_args=default_args,
	description = "this dag will retrieve new News articles and update our visualization",
	schedule_interval = timedelta(hours = 1)
	)


c = BaseHook.get_connection('local_mysql')
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
    id = Column(Integer, primary_key=True)

newsapi = NewsApiClient(api_key = news_api_key)

#Collect News Data

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

today = date.today()
today = today.isoformat()
def clean_news():
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

t8 = python_operator(task_id = "collect news",
	python_callable = clean_news,
	dag = dag)





#Dashboard

def dashboard_creation():
	pass

t11 = python_operator(task_id = "Dashboard"
	python_callable = dashboard_creation,
	dag = dag)







