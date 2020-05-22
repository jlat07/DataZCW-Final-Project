import pandas as pd     
import plotly           
import plotly.express as px

import dash 
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

app = dash.Dash(__name__)


df = pd.read_csv(".csv")
df['Date'] = pd.to_datetime(df['Date'])
df['Date'] = df['Date'].dt.year
df = df.set_index('Date')


app.layout = html.Div([

    html.Div([
        dcc.Graph(id='')
    ]),

    html.Div([
        html.Label(['Choose Years of Border Crossings into the USA:'],
                    style={'font-weight': 'bold'}),
        html.P(),
        dcc.RangeSlider(
            id='my-range-slider', # any name you'd like to give it
            marks={
                1996: '1996',     # key=position, value=what you see
                2000: '2000',
                2004: '2004',
                2008: '2008',
                2012: '2012',
                2016: {'label': '2016', 'style': {'color':'#f50', 'font-weight':'bold'}},
                2018: '2018',
            },
            step=1,                # number of steps between values
            min=1996,
            max=2016,
            value=[1998,2000],     # default value initially chosen
            dots=True,             # True, False - insert dots, only when step>1
            allowCross=False,      # True,False - Manage handle crossover
            disabled=False,        # True,False - disable handle
            pushable=2,            # any number, or True with multiple handles
            updatemode='mouseup',  # 'mouseup', 'drag' - update value method
            included=True,         # True, False - highlight handle
            vertical=False,        # True, False - vertical, horizontal slider
            verticalHeight=900,    # hight of slider (pixels) when vertical=True
            className='None',
            tooltip={'always visible':False,  # show current slider values
                     'placement':'bottom'},
            ),
    ]),

])

#---------------------------------------------------------------

@app.callback(
    Output('our_graph','figure'),
    [Input('my-range-slider','value')]
)

def build_graph(years):

    dff = df.loc[years[1]:years[0]]
    dff = dff[(dff['sentiment_score']=='1)]
    dff = dff[(dff['State']=='Vermont') | (dff['State']=='Idaho')]
    # print(dff[:5])

    fig = px.bar(dff, x="State", y="Value", color='Port Name')

    fig.update_layout(yaxis={'title':'Incoming Border Crossings'},
                      title={'text':'Border Crossing into the United States',
                      'font':{'size':28},'x':0.5,'xanchor':'center'})
    return fig

#---------------------------------------------------------------

if __name__ == '__main__':
    app.run_server(debug=False)