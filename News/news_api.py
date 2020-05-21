import requests
import os
from datetime import date
from dotenv import load_dotenv
from newsapi import NewsApiClient


today = date.today()
today = today.isoformat()

# Init
load_dotenv()
newsapi = NewsApiClient(api_key = os.getenv("NEWS_API_KEY"))

# /v2/top-headlines
top_headlines = newsapi.get_top_headlines(q='corona',
                                          sources='abc-news')
                                        

# /v2/everything
all_articles = newsapi.get_everything(q='covid-19, stock',
                                      sources='abc-news',
                                      from_param='2020-05-01',
                                      to=today,
                                      language='en',
                                      sort_by='relevancy',
                                      page=2)

# /v2/sources
# print(top_headlines)

def print_articles(x):
    for articles in x:
        print(articles)

print(top_headlines)
print('Break')
print(all_articles)
