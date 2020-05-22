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
    dcc.Loading(dcc.Store(id='twitter_df', storage_type='memory')),
    html.Br(),
    dbc.Row([
        dbc.Col([
            html.A([
                html.Img('src=https://avatars2.githubusercontent.com/u/13836040?s=200&v=4',
                         width=200, style={'display': 'inline-block'}),
            ],),
            html.Br(),
        ], lg=2, xs=11, style={'textAlign': 'center'}),
        dbc.Col([
            html.Br(),
            html.H1("Covid-19 Sentiment Dasboard", style={'text-align': 'center'}),

    dcc.Dropdown(id="select_freq_amountt",
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
            html.Br(),
            html.H2(id='wtd_freq_chart_title',
                    style={'textAlign': 'center'}),
            dcc.Loading([
                dcc.Graph(id='wtd_freq_chart',
                            config={'displayModeBar': False},
                            figure={'layout': go.Layout(plot_bgcolor='#eeeeee',
                                                        paper_bgcolor='#eeeeee')
                                    }),
            ]),
        ], label='Text Analysis', id='text_analysis_tab'),
    html.Div(id='freq_container', children=[]),
    html.Br(),

    dcc.Graph(id='word_freq_bar_chart', figure={})

                    ]),
    html.Br(),
    dbc.Row([
        dbc.Col(lg=2, xs=10),
        dbc.Col([
           dcc.Dropdown(id='search_type',
                        placeholder='Search Type',
                        options=[{'label': c, 'value': c}
                                 for c in ['Search Tweets',
                                           'Search Users',
                                           'Get User Timeline']])
        ], lg=2, xs=10),
        dbc.Col([
            dbc.Input(id='twitter_search',
                      placeholder='Search query'),
        ], lg=2, xs=10),
        dbc.Col([
            dbc.Input(id='twitter_search_count',
                      placeholder='Number of results', type='number'),

        ], lg=2, xs=10),
        dbc.Col([
            dcc.Dropdown(id='twitter_search_lang', placeholder='Language',
                         options=lang_options,
                         style={'position': 'relative', 'zIndex': 15}
                         ),
        ], lg=2, xs=10),
        dbc.Col([
            dbc.Button(id='search_button', children='Submit', outline=True),
        ], lg=2, xs=10),
    ]),
html.Div([

    html.H2("Covid-19 Sentiment Dasboard", style={'text-align': 'center'}),

    dcc.Dropdown(id="select_sentiment",
                 options=[
                     {"label": "Positive", "value": 1},
                     {"label": "Neutral", "value": 0},
                     {"label": "Negative", "value": -1}],
                 multi=False,
                 value=1,
                 style={'width': "40%"}
                 ),

    html.Div(id='sentiment_container', children=[]),
    html.Br(),

    dcc.Graph(id='sentiment_map', figure={})
]),

# ------------------------------------------------------------------------------
# Connect the word freq bar chart with with Dash Components
@app.callback(
    [Output(component_id='freq_container', component_property='children'),
     Output(component_id='word_freq_bar_chart', component_property='figure')],
    [Input(component_id='select_freq_amountt', component_property='value')]
            )

def update_graph(option_select):

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
    stopwords = list(STOPWORDS) + ["made", "now", "rt", "covid19", 'to', 'say', 'sort', 'right', 'now']
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
    container = f"Most Frequent Word was {m_o}"
    # Bar Graph
   
    fig = px.bar(word_freq_df, x='word', y='count',
                hover_data=['count', 'word'], color='count',
                labels={'words':'Words'}, height=400,
                orientation='v')

    return container, fig
# ------------------------------------------------------------------------------
# Connect the sentiment heat map with with Dash Components

@app.callback(
    [Output(component_id='sentiment_container', component_property='children'),
    Output(component_id='sentiment_map', component_property='figure')],
    [Input(component_id='select_sentiment', component_property='value')]
)

def update_graph(option_select):
    print(option_select)
    print(type(option_select))

    container = f"Current sentiment being shown: {option_select}"

    dff = twitter_df.copy()
    dff = dff[dff["score"] == option_select]

    fig = px.choropleth(
            data_frame=dff,
            locationmode="USA-states",
            locations="state",
            scope="usa",
            color='score',
            range_color=(-1, 1),
            hover_data=['location', 'sentiment'],
            color_continuous_scale=px.colors.sequential.YlOrRd,
            labels={'sentiment': 'Sentiment'},
            template='plotly_dark'  #['ggplot2', 'seaborn', 'simple_white', 'plotly', 'plotly_white', 'plotly_dark', 'presentation', 'xgridoff', 'ygridoff', 'gridon', 'none']
    ) 

    return container, fig

# ------------------------------------------------------------------------------
# Connect the  with Dash Components

# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)