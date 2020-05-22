from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash_operator import BashOperator
from airflow import DAG
from airflow.utils.dates import days_ago
import airflow.hooks.S3_hook
from airflow.hooks.base_hook import BaseHook
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
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from dash_table import DataTable
from dash_table.FormatTemplate import Format
from matplotlib import rcParams
from plotly.subplots import make_subplots
from wordcloud import WordCloud, STOPWORDS
import collections
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px 
import re
load_dotenv()
analyser = SentimentIntensityAnalyzer()
stop_words = list(set(stopwords.words('english')))
nltk.download('stopwords')
nltk.download('punkt')
today = date.today()
today = today.isoformat()
news_api_key = os.getenv("NEWS_API_KEY")
newsapi = NewsApiClient(api_key = news_api_key)
jupyter_location_string = "/Users/jkocher/Documents/projects/DataZCW-Final-Project/Final_Project/Dashboard/getting_df.ipynb"
executed_location_string = "/Users/jkocher/Documents/projects/DataZCW-Final-Project/Final_Project/Dashboard/report.ipynb"

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


def clean_news():
	now = datetime.now()
	start_date = datetime.now()-timedelta(hours=1)
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
			published_date = datetime.strptime(published_date,"%Y-%m-%dT%H:%M:%SZ")
			published_date = datetime.timestamp(published_date)*1000
			author = str(article.get('author'))
			sentiment = str(add_sentiment(content))
			score = str(add_score(content))
			aut_title = str(str(author)+ " " + str(title))
			message_sql = articles(author=author, title=title, content=content, date=published_date, sentiment = sentiment, score= score,  unique_identify = aut_title)
			Session = sessionmaker(bind=engine)
			session = Session()
			session.add(message_sql)
			session.commit()

t1 = PythonOperator(task_id = "collect_news",
	python_callable = clean_news,
	dag = dag)


#Dashboard

t2 = BashOperator(
	task_id="run_jupyter_notebook",
	bash_command = "papermill /Users/jkocher/Documents/projects/DataZCW-Final-Project/Final_Project/Dashboard/getting_df.ipynb /Users/jkocher/Documents/projects/DataZCW-Final-Project/Final_Project/Dashboard/report.ipynb",
	dag = dag)

t1 >> t2





