import dash
from dash.dependencies import Input, Output
import dash_html_components as html
import dash_core_components as dcc
import dash_daq as daq

import plotly.graph_objs as go
import numpy as np
import serial
from serial.tools import list_ports

from ardu_accel import get_data

from flask import request


try:
    for port in list_ports.comports():
        if port.description == "Circuit Playground Express":
            cpe_device = port.device
            print("Adafruit board found: " + cpe_device)

    cpe = serial.Serial(cpe_device)
except Exception as e:
    print(e)
    print("Unable to locate Circuit Playground Express")
    raise
    # TODO display this warning in the app and handle it better


x = np.zeros(100)
y = np.zeros(100)
mockdata = [{'x': x,
  'y': y,
  'type': 'line',
  'showscale': False,
  'colorscale': [[0, 'rgba(255, 255, 255,0)'], [1, 'rgba(0,0,255,1)']]}]


class ReadLine:
    """ from https://github.com/pyserial/pyserial/issues/216#issuecomment-369414522 """
    def __init__(self, s):
        self.buf = bytearray()
        self.s = s

    def readline(self):
        i = self.buf.find(b"\n")
        if i >= 0:
            r = self.buf[:i+1]
            self.buf = self.buf[i+1:]
            return r
        while True:
            i = max(1, min(2048, self.s.in_waiting))
            data = self.s.read(i)
            i = data.find(b"\n")
            if i >= 0:
                r = self.buf + data[:i+1]
                self.buf[0:] = data[i+1:]
                return r
            else:
                self.buf.extend(data)

app = dash.Dash()

app.config['suppress_callback_exceptions'] = True

server = app.server



app.layout = html.Div(id='container', children=[
    html.Div([
        html.H2('Realtime arduino data',
        style={'marginLeft':'40px'})
    ], className='banner', id='header'),

    daq.Gauge(
        id='gauge',
        max=20,
        value=6,
        min=-20
    ),

    dcc.Graph(
        id='oscope-graph',
        figure=dict(
            data=mockdata,
            layout=go.Layout(
                xaxis={'title': 's', 'color': '#506784',
                       'titlefont': dict(
                           family='Dosis',
                           size=15,
                       ), 'autorange': False, 'range': [0, 10]},
                yaxis={'title': 'Voltage (mV)', 'color': '#506784',
                       'titlefont': dict(
                           family='Dosis',
                           size=15,
                        ), 'autorange': False, 'range': [-20, 20]},
                margin={'l': 40, 'b': 40, 't': 0, 'r': 50},
                plot_bgcolor='#F3F6FA',
            )
        ),
        config={'displayModeBar': True,
                'modeBarButtonsToRemove': ['pan2d',
                                           'zoomIn2d',
                                           'zoomOut2d',
                                           'autoScale2d',
                                           'hoverClosestCartesian',
                                           'hoverCompareCartesian']}
    ),
    dcc.Interval(id='update-data', interval=200, n_intervals=0),
])

# Callback means this fuction will get triggered by the interval timer
# And the output of the function will be sent to the oscope-graph
@app.callback(
        [Output('oscope-graph', 'figure'),
        Output('gauge', 'value')],
        [Input('update-data', 'n_intervals')])
def update_data(value):
    """get live serial data"""
    # try:
    #     rl = ReadLine(cpe)
    #     serialin = rl.readline()
    #     gz = float(serialin.decode('utf-8').split(" ")[5])
    #     print(gz)
    # except (serial.SerialException, IndexError):
    #     gz = 0
    #     pass
    gz = 0

    #TODO push data into figure for live chart
    figure = {
        'data': get_data(cpe),
        'layout': go.Layout(
            xaxis={'title': 'X-accel (g)', 'color': '#506784',
                   'titlefont': dict(
                       family='Dosis',
                       size=15,
                   ), 'autorange': False, 'range': [0, 10]},
            yaxis={'title': 'Y-accel (g)', 'color': '#506784',
                   'titlefont': dict(
                       family='Dosis',
                       size=15,
                   ), 'autorange': False, 'range': [-20, 20]},
            margin={'l': 40, 'b': 40, 't': 0, 'r': 50},
            plot_bgcolor='#F3F6FA',)
    }
    return figure, gz


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
    app.run_server(port=8000, debug=True)
