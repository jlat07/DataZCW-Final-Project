from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from dash_table import DataTable
from dash_table.FormatTemplate import Format
from matplotlib import rcParams
from plotly.subplots import make_subplots
from wordcloud import WordCloud, STOPWORDS
import advertools as adv
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


regex_dict = {'Emoji': adv.emoji.EMOJI_RAW,
            'Mentions': adv.regex.MENTION_RAW,
            'Hashtags': adv.regex.HASHTAG_RAW,}

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])

app.layout = html.Div([
    dcc.Loading(dcc.Store(id='df', storage_type='memory')),
    html.Br(),
    dbc.Row([
        dbc.Col([
            html.A([
                html.Img(src='https://avatars2.githubusercontent.com/u/13836040?s=200&v=4',
                        width=200, style={'display': 'inline-block'}),
            ]),
            html.Br(),
        ], lg=2, style={'textAlign': 'center'}),
        dbc.Col([
            html.Br(),
            html.H1('Covid-19 Sentiment Anylsis',
                    style={'textAlign': 'center'})
        ], lg=9),
    ], style={'margin-left': '1%'}),
    html.Br(),
    dbc.Row([
        dbc.Col(lg=2),
        dbc.Col([
           dcc.Dropdown(id='search_type',
                        placeholder='Search Type',
                        options=[{'label': c, 'value': c}
                                for c in ['Search Tweets',
                                        'Search Articles']])
        ], lg=2),
        dbc.Col([
            dbc.Input(id='search_word',
                    placeholder='Search query'),
        ], lg=2),
        dbc.Col([
            dbc.Input(id='max_entries',
                    placeholder='Max number of results?', type='number'),
    ], lg=2),
    dbc.Col([
        dbc.Button(id='search_button', children='Submit', outline=True),
        ], lg=2),
    ]),
    html.Hr(),
    dbc.Container([
        dbc.Col(lg=2),
        dbc.Tabs([
            dbc.Tab([
                html.Br(),
                dbc.Row([
                    dbc.Col([
                        dbc.Label('Data Type:'),
                        dcc.Dropdown(id='text_columns',
                                    placeholder='Data Type',
                                    value='text'),
                    ], lg=3),
                    dbc.Col([
                        dbc.Label('Weighted by:'),
                        dcc.Dropdown(id='numeric_columns',
                                    placeholder='Numeric Column',
                                    value='score'),
                    ], lg=3),
                    dbc.Col([
                        dbc.Label('Misc Dropdown:'),
                        dcc.Dropdown(id='regex_options',
                                    options={'label': 'Misc', 'value': None},
                                    value=None),
                    ], lg=3),
                ]),
                html.Br(),
                html.H2(id='word_freq_title',
                        style={'textAlign': 'center'}),
                dcc.Loading([
                    dcc.Graph(id='twitter_word_freq',
                            figure={}
                    ),
                ]),
            ], label='Word Frequency', id='word_frequency_tab'),
            dbc.Tab([
                html.H3(id='total_entries', style={'textAlign': 'center'}),
                dcc.Loading([
                    dcc.Graph(id='heat_map',
                            config={'displayModeBar': False},
                            figure={}
                    ),
                ]),
            ], tab_id='user_analysis_tab', label='Sub Plots'),
            dbc.Tab([
                html.Br(),
                html.Iframe(src="",
                        width=595, height=485,
                        style={'margin-left': '30%'})

            ], label='Misc', tab_style={'fontWeight': 'bold'})
        ], id='tabs'),
    ]),
    html.Hr(), html.Br(),
    dbc.Row([
        dbc.Col([
            html.Br(),
            dcc.Loading(
                DataTable(id='table', sort_action='native',
                        virtualization=True,
                        fixed_rows={'headers': True},
                        style_cell={'width': '200px',
                                    'font-family': 'Source Sans Pro',
                                    'backgroundColor': '#eeeeee'}),
            ),
        ], lg=9, style={'position': 'relative', 'zIndex': 1,'margin-left': '1%'}),
    ] + [html.Br() for x in range(30)]),
], style={'backgroundColor': '#eeeeee'}
)

# Store data in memory
@app.callback(Output('df', 'data'),
            [Input('search_button', 'submit_search')],
            [State('search_type', 'value'),
            State('search_word', 'value'),
            State('max_entries', 'value')]
)

def data_base_query(submit_search, search_type, query, count):
    if search_type == 'Search Tweets':
        twitter_df = pd.read_csv('/Users/jthompson/dev/DataZCW-Final-Project/Dashboard/twitter_sample_data.csv', index_col=0)
        twitter_df = twitter_df.drop_duplicates()
        df = twitter_df[twitter_df['content'].str.contains(query)]
        return df

    elif search_type == 'Search Articles':
        article_df = pd.read_csv('/Users/jthompson/dev/DataZCW-Final-Project/Dashboard/news_article_sample_data.csv', index_col=0)
        article_df = article_df.drop_duplicates()
        df = article_df[article_df['content'].str.contains(query)]
        return df

@app.callback(Output('word_freq_title', 'children'),
            Input('df', 'data')
)

def display_wtd_freq_chart_title(regex, df):
    if regex is None or df is None:
        raise PreventUpdate
    return 'Most Frequently Used ' + regex + ' (' + str(len(df)) +  ' Results)'


@app.callback(Output('total_entries', 'children'),
              [Input('df', 'data'),
               Input('search_type', 'value')]
)

def display_total_entries(df, search_type):
    if df is None:
        raise PreventUpdate

    elif search_type == 'Search Tweets':
        count = df['text'].nunique()
        return 'Number of Tweets: ' + str(count)

    elif search_type == 'Search Articles':
        count = df['content'].nunique()
        return 'Number of Articles: ' + str(count)

@app.callback(Output(component_id='twitter_word_freq', component_property='figure'),
            [Input(component_id='df', component_property='data'),
            Input('search_type', 'value'),
            Input('text_columns', 'value'),
            Input('numeric_columns', 'value'),
            Input('search_type', 'value')]
)

def plot_frequency(df, search_type):

    num_cols = [c for c in df.columns if 'count' in c]
    
    if df is None:
        raise PreventUpdate

    elif search_type == 'Search Tweets':
        text = 'text'
        fig_x = 'location'
        fig_y = 'sentiment_score'
        fig_hover = ['location_abbreviation', 'date']
        fig_color = 'sentiment_score'
        fig_lables = {'sentiment_score':'Sentiment Score'}
        
    elif search_type == 'Search Articles':
        article_text = 'content'
        fig_x = 'location'
        fig_y = 'sentiment_score'
        fig_hover = ['location_abbreviation', 'date']
        fig_color = 'sentiment_score'
        fig_lables = {'sentiment_score':'Sentiment Score'}
       
    word_freq_df = adv.word_frequency(df[text], df[num_col],
                                     regex=regex_dict.get(regex),
                                     phrase_len=phrase_len_dict.get(regex)
                                     or 1)[:20]
    fig = make_subplots(rows=1, cols=2,
                        subplot_titles=['Weighted Frequency',
                                        'Absolute Frequency'])
    fig.append_trace(go.Bar(x=wtd_freq_df['wtd_freq'][::-1],
                            y=wtd_freq_df['word'][::-1],
                            name='Weighted Freq.',
                            orientation='h'), 1, 1)
    wtd_freq_df = wtd_freq_df.sort_values('abs_freq', ascending=False)
    fig.append_trace(go.Bar(x=wtd_freq_df ['abs_freq'][::-1],
                            y=wtd_freq_df['word'][::-1],
                            name='Abs. Freq.',
                            orientation='h'), 1, 2)

    fig['layout'].update(height=600,
                         plot_bgcolor='#eeeeee',
                         paper_bgcolor='#eeeeee',
                         showlegend=False,
                         yaxis={'title': 'Top Words: ' +
                                text_col.replace('_', ' ').title()})
    fig['layout']['annotations'] += ({'x': 0.5, 'y': -0.16,
                                      'xref': 'paper', 'showarrow': False,
                                      'font': {'size': 16},
                                      'yref': 'paper',
                                      'text': num_col.replace('_', ' ').title()
                                      },)
    fig['layout']['xaxis']['domain'] = [0.1, 0.45]
    fig['layout']['xaxis2']['domain'] = [0.65, 1.0]
    return fig

# Article Analysis Sub Plots
@app.callback(Output('heat_map', 'figure'),
              Input('df', 'data'),
)

def plot_heat_map(df):
        
    fig = 'Heat Map'
    # subplot_titles = ['Followers Count', 'Statuses Count',
    #                   'Friends Count', 'Favourites Count',
    #                   'Verified', 'Tweet Source',
    #                   'Article Created At']
    # df = pd.DataFrame(df).drop_duplicates('author')
    # fig = make_subplots(rows=2, cols=4,
    #                     subplot_titles=subplot_titles)
    # for i, col in enumerate(subplot_titles[:4], start=1):
    #     col = ('article_' + col).replace(' ', '_').lower()
    #     fig.append_trace(go.Histogram(x=df[col], nbinsx=30,name='Articles'),
    #                      1, i)
    # for i, col in enumerate(subplot_titles[4:7], start=5):
    #     if (i == 6) and (search_type == 'Search Articles'):
    #         continue
    #     if col == 'Tweet Source':
    #         col = 'tweet_source'
    #     else:
    #         col = ('article_' + col).replace(' ', '_').lower()
    #     fig.append_trace(go.Bar(x=df[col].value_counts().index[:14], width=0.9,
    #                             y=df[col].value_counts().values[:14],
    #                             name='Articles'), 2, i-4)
    # fig.append_trace(go.Histogram(x=df['date'],name='Articles',
    #                               nbinsx=30, ), 2, 4)

    # fig['layout'].update(height=600,
    #                      yaxis={'title': 'Number of Articles' + (' ' * 50) + ' .'
    #                             },
    #                      width=1200,
    #                      plot_bgcolor='#eeeeee',
    #                      paper_bgcolor='#eeeeee',
    #                      showlegend=False)
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)