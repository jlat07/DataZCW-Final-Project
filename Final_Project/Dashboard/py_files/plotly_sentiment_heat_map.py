import sqlalchemy
import pymysql
from sqlalchemy import create_engine
import dash  
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

import pandas as pd
import plotly.express as px 
import plotly.graph_objects as go
from wordcloud import WordCloud, STOPWORDS

us_state_abbrev = {
    'Alabama': 'AL',
    'Alaska': 'AK',
    'American Samoa': 'AS',
    'Arizona': 'AZ',
    'Arkansas': 'AR',
    'California': 'CA',
    'Colorado': 'CO',
    'Connecticut': 'CT',
    'Delaware': 'DE',
    'District of Columbia': 'DC',
    'Florida': 'FL',
    'Georgia': 'GA',
    'Guam': 'GU',
    'Hawaii': 'HI',
    'Idaho': 'ID',
    'Illinois': 'IL',
    'Indiana': 'IN',
    'Iowa': 'IA',
    'Kansas': 'KS',
    'Kentucky': 'KY',
    'Louisiana': 'LA',
    'Maine': 'ME',
    'Maryland': 'MD',
    'Massachusetts': 'MA',
    'Michigan': 'MI',
    'Minnesota': 'MN',
    'Mississippi': 'MS',
    'Missouri': 'MO',
    'Montana': 'MT',
    'Nebraska': 'NE',
    'Nevada': 'NV',
    'New Hampshire': 'NH',
    'New Jersey': 'NJ',
    'New Mexico': 'NM',
    'New York': 'NY',
    'North Carolina': 'NC',
    'North Dakota': 'ND',
    'Northern Mariana Islands':'MP',
    'Ohio': 'OH',
    'Oklahoma': 'OK',
    'Oregon': 'OR',
    'Pennsylvania': 'PA',
    'Puerto Rico': 'PR',
    'Rhode Island': 'RI',
    'South Carolina': 'SC',
    'South Dakota': 'SD',
    'Tennessee': 'TN',
    'Texas': 'TX',
    'Utah': 'UT',
    'Vermont': 'VT',
    'Virgin Islands': 'VI',
    'Virginia': 'VA',
    'Washington': 'WA',
    'West Virginia': 'WV',
    'Wisconsin': 'WI',
    'Wyoming': 'WY'
}

app = dash.Dash(__name__)
app = dash.Dash(external_stylesheets=[dbc.themes.CYBORG])   # DARKLY, LUX, SOLAR, FLATLY, MINTY, CYBORG

# ------------------------------------------------------------------------------
# Import and clean data (importing csv into pandas)
engine = create_engine('mysql+pymysql://root:zipcoder@localhost/twitter')

df = pd.read_sql("sentiments", con = engine)
# ------------------------------------------------------------------------------
# App layout

app.layout = html.Div([

    html.H1("Covid-19 Sentiment Dasboard", style={'text-align': 'center'}),

    dcc.Dropdown(id="select_sentiment",
                 options=[
                     {"label": "Positive", "value": "Positive"},
                     {"label": "Negative", "value": "Negative"},
                     {"label": "All", "value": "All"}],
                 multi=False,
                 value="Positive",
                 style={'width': "40%"}
                ),

    html.Div(id='output_container', children=[]),
    html.Br(),

    dcc.Graph(id='sentiment_map', figure={})

                    ])

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
    if option_select != "All":
        dff = dff[dff["sentiment"] == option_select]
    else:
        range_col = (-1,1)
    if option_select == "Positive":
        range_col = (0,1)
    if option_select == "Negative":
        range_col = (-1,0)
    dff["score"] = dff["score"].astype(float)
    dff = dff.groupby("state").agg({"score":"mean"})
    dff = dff.reset_index()
    dff = dff[dff.state != "N/A"]
    dff['abbrev'] = dff['state'].map(us_state_abbrev)
    print(dff)


    fig = px.choropleth(
            data_frame=dff,
            locationmode="USA-states",
            locations='abbrev',
            scope="usa",
            color="score",
            range_color=range_col,
            hover_data=['state','score'],
            color_continuous_scale=px.colors.sequential.YlOrRd,
            labels={'color': 'Sentiment'},
            template='plotly_dark') 

    return container, fig
# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(port = 8055, debug=True)