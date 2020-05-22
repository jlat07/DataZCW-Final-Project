import sqlalchemy
import pymysql
from sqlalchemy import create_engine
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


app1 = dash.Dash(__name__)
app1 = dash.Dash(external_stylesheets=[dbc.themes.CYBORG])   # DARKLY, LUX, SOLAR, FLATLY, MINTY, CYBORG

# ------------------------------------------------------------------------------
# Import and clean data (importing csv into pandas)
engine = create_engine('mysql+pymysql://root:zipcoder@localhost/twitter')

twitter_df = pd.read_sql("sentiments", con = engine)
twitter_df = twitter_df.drop_duplicates()
# ------------------------------------------------------------------------------
# App layout

app1.layout = html.Div([

    html.H1("Covid-19 Sentiment Dasboard", style={'text-align': 'center'}),

    dcc.Dropdown(id="select_count",
                 options=[
                     {"label": "5 Most Freq. Words", "value": 5},
                     {"label": "10 Most Freq. Words", "value": 10},
                     {"label": "25 Most Freq. Words", "value": 25},
                     {"label": "50 Most Freq. Words", "value": 50},
                     {"label": "75 Most Freq. Words", "value": 75},
                     {"label": "100 Most Freq. Words", "value": 100}],
                 multi=False,
                 value=5,
                 style={'width': "40%"}
                ),

    html.Div(id='output_container', children=[]),
    html.Br(),

    dcc.Graph(id='sentiment_map', figure={})

                    ])


# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components
@app1.callback(
    [Output(component_id='output_container', component_property='children'),
     Output(component_id='sentiment_map', component_property='figure')],
    [Input(component_id='select_count', component_property='value')]
            )

def update_graph(option_select):


    container = f"Current sentiment being shown: {option_select}"

    dff = twitter_df.copy()

    
    words = []
    counts = []

    # most_common word amout
    x = option_select
    # gather all tweets
    all_words = ' '.join(dff['text'].str.lower())
    #remove links, #hashtags, @, :
    cleaned_words = re.sub(r'http\S+', '', all_words)
    cleaned_word1 = re.sub(r"#(\w+)", ' ', cleaned_words, flags=re.MULTILINE)
    cleaned_word2 = re.sub(r"@(\w+)", ' ', cleaned_word1, flags=re.MULTILINE)
    cleaned_tweets = re.sub(r" : (\w+)", ' ', cleaned_word2, flags=re.MULTILINE)
    # Stop Words
    stopwords = list(STOPWORDS) + ["made","-","&","covid19.", "coronavirus", "covid-19","#covid19","covid", "#coronavirus", "now", "rt", "covid19", 'to', 'say', 'sort', 'right', 'now']
    # Filter Words
    filtered_words = [word for word in cleaned_words.split() if word not in stopwords]
    # Counted words
    counted_words = collections.Counter(filtered_words)
    # Four loop to count most common
    for letter, count in counted_words.most_common(x):
        words.append(letter)
        counts.append(count)
    #df to be read by px
    word_freq_df = pd.DataFrame(list(zip(words, counts)), 
               columns =['word', 'count']) 
    # most occuring word
    most_occuring = word_freq_df.nlargest(1, ['count'])
    # string 
    m_o = most_occuring['word'].item()
    #containter to return call back
    container = f"{option_select} Most Frequently Used Words\n Most Frequent Word was {m_o}"
   # Bar Graph
   
    fig = px.bar(word_freq_df, x='word', y='count',
                hover_data=['count', 'word'], color='count',
                labels={'words':'Words'}, height=400,
                orientation='v')

    return container, fig


# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app1.run_server(port=8054,debug=True)