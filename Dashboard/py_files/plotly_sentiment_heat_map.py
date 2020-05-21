import dash  
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

import pandas as pd
import plotly.express as px 
import plotly.graph_objects as go
from wordcloud import WordCloud, STOPWORDS


app = dash.Dash(__name__)
app = dash.Dash(external_stylesheets=[dbc.themes.CYBORG])   # DARKLY, LUX, SOLAR, FLATLY, MINTY, CYBORG

# ------------------------------------------------------------------------------
# Import and clean data (importing csv into pandas)
df = pd.read_csv('/Users/jthompson/dev/DataZCW-Final-Project/Dashboard/twitter_sample_data.csv', index_col=0)
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

    dcc.Graph(id='sentiment_map', figure={})

                    ])
# app.layout = html.Div([

#     html.H1("Covid-19 Sentiment Dasboard", style={'text-align': 'center'}),

#     dcc.Dropdown(id="select_sentiment",
#                  options=[
#                      {"label": "Positive", "value": 1},
#                      {"label": "Neutral", "value": 0},
#                      {"label": "Negative", "value": -1}],
#                  multi=False,
#                  value=1,
#                  style={'width': "40%"}
#                  ),

#     html.Div(id='output_container', children=[]),
#     html.Br(),

#     dcc.Graph(id='sentiment_map', figure={})
# ])

# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components
@app.callback(Output(component_id='sentiment_map', component_property='figure'),
            (Input(component_id='select_sentiment', component_property='value')))

def update_graph(option_select):
    print(option_select)
    print(type(option_select))

    container = f"Current sentiment being shown: {option_select}"

    dff = df.copy()


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
if __name__ == '__main__':
    app.run_server(debug=True)