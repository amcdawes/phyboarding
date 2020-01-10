# based on: https://github.com/bokeh/bokeh/tree/master/examples/app/ohlc
# Waits for block of data over serial to plot in bokeh graph
# use with Arduino accel_logger code on Circuit Playgroud Express
# run with `bokeh serve arduinolive`

import numpy as np

from bokeh.driving import count
from bokeh.layouts import column, gridplot, row
from bokeh.models import ColumnDataSource, Select, Slider
from bokeh.plotting import curdoc, figure

import serial
from serial.tools import list_ports

for port in list_ports.comports():
    if port.description == "Circuit Playground Express":
        cpe_device = port.device

print(cpe_device)
cpe = serial.Serial(cpe_device)

np.random.seed(1)

source = ColumnDataSource(dict(
    period=[0], ax=[0], ay=[0], az=[0]
))

p = figure(plot_height=500, tools="xpan,xwheel_zoom,xbox_zoom,reset")
# p.x_range.follow = "end"
# p.x_range.follow_interval = 500
# p.x_range.range_padding = 0

p.line(x='period', y='ax', alpha=0.8, line_width=2, color='orange', source=source)

mean = Slider(title="mean", value=0, start=-0.01, end=0.01, step=0.001)
stddev = Slider(title="stddev", value=0.04, start=0.01, end=0.1, step=0.01)

def _get_data(t):
    """ read data from arduino """
    while(True):
        line = cpe.readline()
        if(line == b'DATA\n'):
            datastring = cpe.readline()
            data = datastring.split(b' ')[:-1] # strip last newline char
            datafloats = [float(i) for i in data]
            #print(datafloats)

            period = np.linspace(0,2500,500)
            ax = datafloats
            ay = ax
            az = ax
            break

    #period = source.data['period'][-1] + 0.1
    #ax, ay, az = np.random.random(),np.random.random(),np.random.random()

    return period, ax, ay, az

@count()
def update(t):
    period, ax, ay, az = _get_data(t)

    # new_data = dict(
    #     period=[period],
    #     ax=[ax],
    #     ay=[ay],
    #     az=[az],
    # )

    source.data = dict(ax=ax, ay=ay, az=az, period=period)

curdoc().add_root(column(row(mean, stddev), gridplot([[p]], toolbar_location="left", plot_width=1000)))
curdoc().add_periodic_callback(update, 500) # This was originally too fast? was 50
curdoc().title = "Live Arduino"
