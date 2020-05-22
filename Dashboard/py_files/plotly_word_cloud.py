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


app = dash.Dash(__name__)
app = dash.Dash(external_stylesheets=[dbc.themes.CYBORG])   # DARKLY, LUX, SOLAR, FLATLY, MINTY, CYBORG

# ------------------------------------------------------------------------------
# Import and clean data (importing csv into pandas)
twitter_df = pd.read_csv('/Users/jthompson/dev/DataZCW-Final-Project/Dashboard/twitter_sample_data.csv', index_col=0)
twitter_df = twitter_df.drop_duplicates()
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

# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components

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


@app.callback(Output('image_wc', 'src'), [Input('image_wc', 'id')])

def make_image(b):
    img = BytesIO()
    plot_wordcloud(data=dfm).save(img, format='PNG')
    return 'data:image/png;base64,{}'.format(base64.b64encode(img.getvalue()).decode())


# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)