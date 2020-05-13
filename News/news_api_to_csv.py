from datetime import timedelta, datetime
from dotenv import load_dotenv
import pprint
import pandas as pd
import requests
import os


load_dotenv()
url = 'https://newsapi.org/v2/everything?'
api_key = os.getenv("NEWS_API_KEY")
today = datetime.today()
today = today.isoformat()


# Daily corona news
corona_parameters = {
    'q': 'corona',
    'pageSize': 100,
    'apiKey': api_key,
    'language': 'en',
    'from' : 'today',
}

corona_response = requests.get(url, params = corona_parameters)
corona_response = corona_response.json()


# Daily covid news
covid_parameters = {
    'q': 'Covid-19',
    'pageSize': 100,
    'apiKey': api_key,
    'language': 'en',
    'from' : 'today'
    
}

covid_response = requests.get(url, params = covid_parameters)
covid_response = covid_response.json()
print(covid_response)

"""
# <Misc>
<Misc> = {
    'q': '<Misc>',
    'pageSize': 100,
    'apiKey': api_key,
    'language': 'en',
    'from' : 'today',
}

<Misc> = requests.get(url, params = <Misc>)
<Misc> = <Misc>.json()
"""

# Webscraping cleaning 

print(covid_response.keys())

# JSON article key
corona_articles = corona_response['articles']
covid_articles = covid_response['articles']
#<Misc> = <Misc>['articles']

# Extracting the relevant information from the list of lists 
def get_articles(file): 
    article_results = []
    
    for i in range(len(file)):
        article_dict = {}
        article_dict['title'] = file[i]['title']
        article_dict['author'] = file[i]['author']
        article_dict['source'] = file[i]['source']
        article_dict['description'] = file[i]['description']
        article_dict['content'] = file[i]['content']
        article_dict['pub_date'] = file[i]['publishedAt']
        article_dict['url'] = file[i]["url"]
        
        article_results.append(article_dict)
    return article_results
        

# Convert the article scrape into customized dataframes 
corona_response = pd.DataFrame(get_articles(corona_response))
covid_response = pd.DataFrame(get_articles(covid_response))
#<Misc> = pd.DataFrame(get_articles(<Misc>))


# Extracts the media source from the dictionared column "source".
def source_getter(df):
    
    source = []
    for source_dict in df['source']:
        source.append(source_dict['name'])
   
    df['source'] = source


# Update publicaiton date
corona_response['pub_date'] = pd.to_datetime(corona_response['pub_date']).apply(lambda x: x.date())
covid_response['pub_date'] = pd.to_datetime(covid_response['pub_date']).apply(lambda x: x.date())
#<Misc>['pub_date'] = pd.to_datetime(<Misc>['pub_date']).apply(lambda x: x.date())

# Combining all news
all_covid_news = pd.concat([corona_response,covid_response])
                                        #<Misc>])

#Converting Dataframe into CSV
all_covid_news.to_csv(f'{today}all_covid_news.csv', index = False)
corona_response.to_csv(f'{today}corona_news.csv', index = False)
covid_response.to_csv(f'{today}covid_news.csv', index = False)
#<Misc>.to_csv(f'{today}<Misc>_news.csv', index = False)