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
df = pd.read_csv("/Users/jthompson/dev/DataZCW-Final-Project/Data/twitter_data_analysis2020-05-09-18.csv")

# print(df)

# ------------------------------------------------------------------------------
# App layout
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = html.Div([
    dcc.Slider(
        id='my-slider',
        min=0,
        max=20,
        step=0.5,
        value=10,
    ),
    html.Div(id='slider-output-container')
])


@app.callback(
    dash.dependencies.Output('slider-output-container', 'children'),
    [dash.dependencies.Input('my-slider', 'value')])
def update_output(value):
    return 'You have selected "{}"'.format(value)





app.layout = html.Div([

    html.H1("Covid-19 Sentiment Dasboard", style={'text-align': 'center'}),

    dcc.Dropdown(id="slct_month",
                 options=[
                     {"label": "Jan", "value": 1},
                     {"label": "Feb", "value": 2},
                     {"label": "Mar", "value": 3},
                     {"label": "Apr", "value": 4},
                     {"label": "May", "value": 5},
                     {"label": "Jun", "value": 6},
                     {"label": "Jul", "value": 7},
                     {"label": "Aug", "value": 8},
                     {"label": "Sep", "value": 9},
                     {"label": "Oct", "value": 10},
                     {"label": "Nov", "value": 11},
                     {"label": "Dec", "value": 12}],
                 multi=False,
                 value=1,
                 style={'width': "40%"}
                 ),

    html.Div(id='output_container', children=[]),
    html.Br(),

    dcc.Graph(id='Sentiment_Map', figure={})

])


# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components
@app.callback(
    [Output(component_id='slider-output-container', component_property='children'),
     Output(component_id='Sentiment_Map', component_property='figure')],
    [Input(component_id='slct_month', component_property='value')]
)
def update_graph(option_slctd):
    print(option_slctd)
    print(type(option_slctd))

    container = "The month chosen by user was: {}".format(option_slctd)

    dff = df.copy()
    dff = dff[dff["Month"] == option_slctd]
    dff = dff[dff["Sentiment"] == "Positive"]

    # Plotly Express
    fig = px.choropleth(
        data_frame=dff,
        locationmode='USA-states',
        locations='state_code',
        scope="usa",
        color='Sentiment',
        hover_data=['State', 'Sentiment'],
        color_continuous_scale=px.colors.sequential.YlOrRd,
        labels={'Sentiment Value': 'Sentiment'},
        template='plotly_dark'
    )

    # Plotly Graph Objects (GO)
    # fig = go.Figure(
    #     data=[go.Choropleth(
    #         locationmode='USA-states',
    #         locations=dff['state_code'],
    #         z=dff["Sentiment"].astype(float),
    #         colorscale='Reds',
    #     )]
    # )
    #
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