#import datadotworld as dw
import pandas as pd
import pickle
from datetime import timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash_operator import BashOperator
#from airflow.operators.papermill_operator import PapermillOperator
#from airflow.operators.postgres_operator import PostgresOperator
#from airflow.operators.postgres_operator import PostgresHook
from airflow.utils.dates import days_ago
#from datetime import datetime
#import sqlalchemy
#import pymysql
#import papermill as pm
import airflow.hooks.S3_hook
from airflow.hooks.base_hook import BaseHook
from airflow.providers.mysql.operators.mysql import MySqlOperator

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

#Gather twitter data

c = BaseHook.get_connection('local_mysql')

t1 = bash_operator(
	task_id="get_.sql_final_tweets",
	bash_command = ("mysqldump -u " + str(c.login)+" -p"+str(c.password)+" twitter > ~/Desktop/test.sql"),
	dag = dag)

#Delete tweets in most recent batch extraction
t2 = MySqlOperator(
	task_id = "delete_old_tweets",
	sql = "TRUNCATE twitter_stream",
	mysql_conn_id = 'local_mysql',
	database = "twitter")

#Clean twitter Data

def clean_tweets()
	pass

t3 = python_operator(task_id = "clean_tweets",
	python_callable = clean_tweets,
	dag = dag)


#Pass Cleaned Tweets to NLP
def nlp_tweets():
	pass

t4 = python_operator(task_id = "NLP_Tweets"
	python_callable = nlp_Tweets,
	dag = dag)

#Save results of NLP

def NLP_tweets_toDB():
	pass

t5 = python_operator(task_id = "NLP_Tweet_Results_toDB"
	python_callable = nlp_Tweets,
	dag = dag)

#Collect News Data
t6 = bash_operator(
	task_id="get_.sql_final_tweets",
	bash_command = ("mysqldump -u " + str(c.login)+" -p"+str(c.password)+" news > ~/Desktop/test.sql"),
	dag = dag)

#Delete News in most recent batch extraction
t7 = MySqlOperator(
	task_id = "delete_old_tweets",
	sql = "TRUNCATE news_stream",
	mysql_conn_id = 'local_mysql',
	database = "news")

#Clean News Data

def clean_news()
	pass

t8 = python_operator(task_id = "clean_news",
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







