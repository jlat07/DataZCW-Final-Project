import dash  
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import pandas as pd
import plotly.express as px 
import plotly.graph_objects as go


app = dash.Dash(__name__)

# ------------------------------------------------------------------------------
# Import and clean data (importing csv into pandas)
df = pd.read_csv('/Users/jthompson/dev/DataZCW-Final-Project/Dashboard/date_tweets_locations_50.csv', index_col=0)
df['date'] = pd.to_datetime(df['date'])
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
@app.callback(
    [Output(component_id='output_container', component_property='children'),
     Output(component_id='sentiment_map', component_property='figure')],
    [Input(component_id='select_sentiment', component_property='value')]
            )

def update_graph(option_select):
    print(option_select)
    print(type(option_select))

    container = f"Current sentiment being shown: {option_select}"

    dff = df.copy()
    dff = dff[dff["sentiment_score"] == option_select]

    # Plotly Express
    fig = px.choropleth(
        data_frame=dff,
        locationmode="USA-states",
        locations="location_abbreviation",
        scope="usa",
        color='sentiment_score',
        range_color=(-1, 1),
        hover_data=['location', 'sentiment_score'],
        color_continuous_scale=px.colors.sequential.YlOrRd,
        labels={'sentiment_score': 'Sentiment Score'},
        template='plotly_dark')

    #Plotly Graph Objects (GO)
    # fig = go.Figure(
    #     data=[go.Choropleth(
    #         locationmode='USA-states',
    #         locations=dff['location_abbreviation'],
    #         z=dff['sentiment'].astype(float),
    #         colorscale='Reds',
    #     )]
    # )
    
    # fig.update_layout(
    #     title_text="Title",
    #     title_xanchor="center",
    #     title_font=dict(size=24),
    #     title_x=0.5,
    #     geo=dict(scope='usa'),
    # )

    return container, fig


# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)