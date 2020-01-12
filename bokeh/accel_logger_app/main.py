# based on: https://github.com/bokeh/bokeh/tree/master/examples/app/ohlc
# Waits for block of data over serial to plot in bokeh graph
# use with Arduino accel_logger code on Circuit Playgroud Express
# run with `bokeh serve arduinolive`

import numpy as np

#from bokeh.driving import count
from bokeh.layouts import column, gridplot, row
from bokeh.models import ColumnDataSource, Select, Slider, Span
from bokeh.plotting import curdoc, figure

from bokeh.models.tools import HoverTool

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

p.line(x='period', y='ay', alpha=0.8, line_width=2, color='orange', source=source)

m1 = Slider(title="Mark 1", value=10, start=0, end=2500, step=1)
m2 = Slider(title="Mark 2", value=2490, start=0, end=2500, step=1)

# hover = HoverTool()
# hover.tooltips=[
#     ('time', 'period'),
#     ('accel', 'ax'),
# ]

hover = HoverTool(
    tooltips=[
        ( 'time',   '@period{%0.2f}'            ),
        ( 'accel',  '@ay{%0.2f}' )
    ],

    formatters={
        'period'      : 'printf', # use 'datetime' formatter for 'date' field
        'ay' : 'printf'   # use 'printf' formatter for 'adj close' field
    },

    # display a tooltip whenever the cursor is vertically in line with a glyph
    mode='vline'
)

p.add_tools(hover)

def _get_data():
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

def update_markers(attrname, old, new):
    # Get the current slider values
    mark1 = m1.value
    mark2 = m2.value
    ml1 = Span(location=mark1, dimension='height', line_color='red', line_width=3)
    ml2 = Span(location=mark2, dimension='height', line_color='blue', line_width=3)
    # add vertical lines to plot at mark1 and mark2
    p.renderers.extend([ml1, ml2])
    print('updated')

# Add on_change listener to each widget that we're using:
for w in [m1, m2]:
    w.on_change('value', update_markers)


#@count()
def update():
    period, ax, ay, az = _get_data()

    # new_data = dict(
    #     period=[period],
    #     ax=[ax],
    #     ay=[ay],
    #     az=[az],
    # )

    source.data = dict(ax=ax, ay=ay, az=az, period=period)


curdoc().add_root(column(row(m1, m2), gridplot([[p]], toolbar_location="left", plot_width=1000)))
curdoc().add_periodic_callback(update, 500) # This was originally too fast? was 50
# TODO sort out the two callbacks: sliders and periodic. Another way to
# test for new data?
curdoc().title = "Live Arduino"
