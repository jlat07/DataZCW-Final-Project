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
import pandas as pd
import pickle
from datetime import timedelta
from datetime import datetime
import sqlalchemy
from sqlalchemy import create_engine
import pymysql
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker
import requests
import os
from datetime import date
from newsapi import NewsApiClient
import re
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
import nltk
analyser = SentimentIntensityAnalyzer()
stop_words = list(set(stopwords.words('english')))
nltk.download('stopwords')
nltk.download('punkt')


default_args = {
    'owner': 'James Kocher',
    'depends_on_past': False,
    'start_date': datetime.now(),
    'retries': 0
	}

dag = DAG(
	"Final_Project_Pipeline",
	default_args=default_args,
	description = "This dag will get new top 10 every week from billboard, create necessary columns to run through spotify",
	schedule_interval = timedelta(days = 7)
	)


c = BaseHook.get_connection('local_mysql')
engine = create_engine('mysql+pymysql://root:zipcoder@localhost/News')

#set up twitter database

t1 = bash_operator(
	task_id="set_up_sql_tables",
	bash_command = ("mysql -u " + str(c.login)+" -p"+str(c.password)+" < ../twittersetup.sql"),
	dag = dag)

#set up news database

t2 = bash_operator(
	task_id="set_up_sql_tables",
	bash_command = ("mysql -u " + str(c.login)+" -p"+str(c.password)+" < ../newssetup.sql"),
	dag = dag)

news_api_key = 'e5c1081b366a416caa370c85bb04d392'

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


def clean_news():
	today = date.today()
	today = today.isoformat()
	all_articles = newsapi.get_everything(q='covid-19',
		sources='abc-news', 
		from_param='2020-05-01', 
		to=today,
		language='en',
		sort_by='relevancy', 
		page=2)
	num_articles = all_articles.get('totalResults')
	for i in range(num_articles):
		author = all_articles.get('articles')[i].get('author')
		title = all_articles.get('articles')[i].get('title')
		content = all_articles.get('articles')[i].get('content')
		published_date = all_articles.get('articles')[i].get('publishedAt')
		sentiment = add_sentiment(content)
		score = add_score(content)
		message_sql = articles(author=author, title = title, content=content, published_date=published_date, sentiment = sentiment, score= score)
		Session = sessionmaker(bind=engine)
		session = Session()
		session.add(message_sql)
		session.commit()

t8 = python_operator(task_id = "collect news",
	python_callable = clean_news,
	dag = dag)


#Pass Cleaned Tweets to NLP
def nlp_news():
	pass

t9 = python_operator(task_id = "NLP_news"
	python_callable = nlp_news,
	dag = dag)

#Save results of NLP

def NLP_news_toDB():
	pass

t10 = python_operator(task_id = "NLP_news_Results_to_DB"
	python_callable = NLP_news_toDB,
	dag = dag)

#Dashboard

def dashboard_creation():
	pass

t11 = python_operator(task_id = "Dashboard"
	python_callable = dashboard_creation,
	dag = dag)







