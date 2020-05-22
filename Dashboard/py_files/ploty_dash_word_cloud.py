from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from dash_table import DataTable
from dash_table.FormatTemplate import Format
from matplotlib import rcParams
from plotly.subplots import make_subplots
from plotly.offline import init_notebook_mode, plot
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


import plotly.io as pio
pio.renderers


twitter_df = pd.read_csv('/Users/jthompson/dev/DataZCW-Final-Project/Dashboard/twitter_sample_data.csv', index_col=0)
twitter_df = twitter_df.drop_duplicates() 

dff = twitter_df.copy()

words = []
counts = []

# most_common word amout
x = 20
# gather all tweets
all_words = ' '.join(dff['text'].str.lower())
#remove links, #hashtags, @, :
cleaned_words = re.sub(r'http\S+', '', all_words)
cleaned_word1 = re.sub(r"#(\w+)", ' ', cleaned_words, flags=re.MULTILINE)
cleaned_word2 = re.sub(r"@(\w+)", ' ', cleaned_word1, flags=re.MULTILINE)
cleaned_tweets = re.sub(r" : (\w+)", ' ', cleaned_word2, flags=re.MULTILINE)
# Stop Words
stopwords = list(STOPWORDS) + ["made", "now", "rt", "covid19", 'to', 'say', 'sort', 'right', 'now']
# Filter Words
filtered_words = [word for word in cleaned_words.split() if word not in stopwords]
# Counted words

app = dash.Dash(__name__)
app = dash.Dash(external_stylesheets=[dbc.themes.CYBORG])   # DARKLY, LUX, SOLAR, FLATLY, MINTY, CYBORG

# ------------------------------------------------------------------------------
# App layout

app.layout = html.Div([

    html.H1("Covid-19 Sentiment Dasboard", style={'text-align': 'center'}),

    dcc.Dropdown(id="select_sentiment",
                 options=[
                     {"label": "Positive", "value": 1},
                     {"label": "Neutral", "value": 0},
                     {"label": "Negative", "value": -1}],
                 multi=False,
                 value=1,
                 style={'width': "40%"}
                ),

    html.Div(id='output_container', children=[]),
    html.Br(),

    html.Img(id="image_wc")

])

@app.callback(dcc.Output('image_wc', 'src'), [dcc.Input('filtered_words', 'data')])

def plotly_wordcloud(text):
    wc = WordCloud(stopwords = set(STOPWORDS),
                   max_words = 200,
                   max_font_size = 100)
    wc.generate(text)
    
    word_list=[]
    freq_list=[]
    fontsize_list=[]
    position_list=[]
    orientation_list=[]
    color_list=[]

    for (word, freq), fontsize, position, orientation, color in wc.layout_:
        word_list.append(word)
        freq_list.append(freq)
        fontsize_list.append(fontsize)
        position_list.append(position)
        orientation_list.append(orientation)
        color_list.append(color)
        
    # get the positions
    x=[]
    y=[]
    for i in position_list:
        x.append(i[0])
        y.append(i[1])
            
    # get the relative occurence frequencies
    new_freq_list = []
    for i in freq_list:
        new_freq_list.append(i*100)
    new_freq_list
    
    trace = go.Scatter(x=x, 
                       y=y, 
                       textfont = dict(size=new_freq_list,
                                       color=color_list),
                       hoverinfo='text',
                       hovertext=['{0}{1}'.format(w, f) for w, f in zip(word_list, freq_list)],
                       mode="text",  
                       text=word_list
                      )
    
    layout = go.Layout(
                       xaxis=dict(showgrid=False, 
                                  showticklabels=False,
                                  zeroline=False,
                                  automargin=True),
                       yaxis=dict(showgrid=False,
                                  showticklabels=False,
                                  zeroline=False,
                                  automargin=True)
                      )
    
    fig = go.Figure(data=[trace], layout=layout)
    
    return fig

init_notebook_mode(connected=True)
plot(plotly_wordcloud(filtered_words))
