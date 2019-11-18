import dash
from dash.dependencies import Input, Output
import dash_html_components as html
import dash_core_components as dcc
import dash_daq as daq

import plotly.graph_objs as go
import numpy as np
import serial

cpe = serial.Serial("/dev/cu.usbmodem14501", 9600)

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
        id='my-daq-gauge',
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
                       )},
                yaxis={'title': 'Voltage (mV)', 'color': '#506784',
                       'titlefont': dict(
                           family='Dosis',
                           size=15,
                        ), 'autorange': False, 'range': [-10, 10]},
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
    dcc.Interval(id='update-data', interval=100, n_intervals=0),
])

@app.callback(
        [Output('oscope-graph', 'figure'),
        Output('my-daq-gauge', 'value')],
        [Input('update-data', 'n_intervals')])
def update_data(value):
    """get live serial data here"""
    try:
        rl = ReadLine(cpe)
        serialin = rl.readline()
        gz = float(serialin.decode('utf-8').split(" ")[7])
        print(gz)
    except (serial.SerialException, IndexError):
        gz = 0
        pass

    #TODO parse and except serial input
    figure = {
        'data': mockdata,
        'layout': go.Layout(
            xaxis={'title': 's', 'color': '#506784',
                   'titlefont': dict(
                       family='Dosis',
                       size=15,
                   )},
            yaxis={'title': 'Voltage (mV)', 'color': '#506784',
                   'titlefont': dict(
                       family='Dosis',
                       size=15,
                   ), 'autorange': False, 'range': [-10, 10]},
            margin={'l': 40, 'b': 40, 't': 0, 'r': 50},
            plot_bgcolor='#F3F6FA',)
    }
    return figure, gz


if __name__ == '__main__':
    app.run_server(port=8000, debug=True)
