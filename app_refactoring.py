from re import template
from click import style
import dash
from dash.dependencies import Output, Input
import dash_core_components as dcc
import dash_html_components as html
from numpy import average, var
import plotly
import random
import plotly.graph_objs as go
from collections import deque
from dash_extensions import WebSocket
import json
import config
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.io as pio

# This is the code that works for Websockets connection.

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

X = deque(maxlen = 20)
X.append(1)

Y = deque(maxlen = 20)
Y.append(1)
  
app = dash.Dash(__name__,external_stylesheets=[dbc.themes.DARKLY])
app.layout = html.Div(
    [
        html.H1("ETHUSD",        style={
            'textAlign': 'center',
            'color': colors['text']
        }),
        dcc.Graph(id = 'live-graph', animate = True),
        dcc.Interval(
            id = 'graph-update',
            interval = 600,
            n_intervals = 0
        ),
        WebSocket(url=config.WEBSOCKET, id="ws")
    ]
)

@app.callback(Output("ws", "send"),
    [Input('graph-update', 'n_intervals')]
    )
def initialize_socket(n):
    print("llama al socket:", n)
    if (n==1):
        auth_data = {
                "action": "auth",
                "key": config.ALPACA_API_KEY,
                "secret": config.ALPACA_SECRET_KEY,
            }
        return json.dumps(auth_data)
    else:
        listen_message = {"action":"subscribe","trades":["ETHUSD"]}
        return json.dumps(listen_message)
        
@app.callback(
    Output('live-graph', 'figure'),
    [Input("ws", "message")]
    )
def update_graph_scatter(n):
    try: 
        print("valor de la función :",json.loads(n['data'])[0]['p'])
        price=json.loads(n['data'])[0]['p']
    except:
        price=2639
    X.append(X[-1]+1)
    Y.append(price)
  
    data = plotly.graph_objs.Scatter(
            x=list(X),
            y=list(Y)
    )
  
    return {'data': [data],
            'layout' : go.Layout(xaxis=dict(range=[10,20]),yaxis = dict(range = [min(Y),max(Y)]))}
  

if __name__ == '__main__':
    app.run_server()