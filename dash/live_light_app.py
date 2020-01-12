# A Dash app for displaying light levels from a Circuit Playground Express
# Be sure CPE is running firmware from the lightsense folder
# TODO: add stop button and auto-scale enable/disable toggles

import dash
from dash.dependencies import Output, Input
import dash_core_components as dcc
import dash_html_components as html
import plotly
import random
import plotly.graph_objs as go
from collections import deque

from cpe_device import CPEdevice

mycpe = CPEdevice()

X = deque(maxlen=20)
X.append(1)
Y = deque(maxlen=20)
Y.append(1)

default_layout=go.Layout(
    xaxis={'title': 'samples', 'color': '#506784',
           'titlefont': dict(
               family='Dosis',
               size=15,
           ), 'autorange': True},
    yaxis={'title': 'Light Level (arb.)', 'color': '#506784',
           'titlefont': dict(
               family='Dosis',
               size=15,
            ), 'autorange': True},
    margin={'l': 40, 'b': 40, 't': 0, 'r': 50},
    plot_bgcolor='#F3F6FA',
)

app = dash.Dash(__name__)

server = app.server

app.layout = html.Div(
    [
        dcc.Graph(
            id='the-graph',
            animate=False,
            figure=dict(layout=default_layout)
        ),
        dcc.Interval(
            id='do-update',
            interval=100
        ),
    ]
)

@app.callback(Output('the-graph', 'figure'),
              [Input('do-update', 'n_intervals')])
def update_graph_scatter(value):
    # TODO: This is where real data input goes!
    X.append(X[-1]+1)
    # Replace this with the real value from the serial port:
    Y.append(mycpe.get_data())

    data = plotly.graph_objs.Scatter(
            x=list(X),
            y=list(Y),
            name='Scatter',
            mode= 'lines+markers'
            )

    #return {'data': [data],'layout' : go.Layout(xaxis=dict(range=[min(X),max(X)]))}
    return {'data': [data], 'layout' : default_layout}


# Allow shutdown of server:
def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

# to allow POST request to shutdown the server:
# TODO add a button in the app?
@server.route('/shutdown', methods=['POST'])
def shutdown():
    shutdown_server()
    return 'Server shutting down...'

if __name__ == '__main__':
    app.run_server(debug=True)
