import dash
from dash.dependencies import Output, Input
import dash_core_components as dcc
import dash_html_components as html
import plotly
import random
import plotly.graph_objs as go
from collections import deque

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
            ), 'autorange': False, 'range': [0, 10]},
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
    X.append(X[-1]+1)
    Y.append(Y[-1]+Y[-1]*random.uniform(-0.1,0.1))

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