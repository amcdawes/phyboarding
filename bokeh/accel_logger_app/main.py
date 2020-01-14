# based on: https://github.com/bokeh/bokeh/tree/master/examples/app/ohlc
# Waits for block of data over serial to plot in bokeh graph
# use with Arduino accel_logger code on Circuit Playgroud Express
# run with `bokeh serve arduinolive`

import numpy as np
from bokeh.layouts import column, gridplot, row
from bokeh.models import ColumnDataSource, Select, Slider, Span, Paragraph
from bokeh.plotting import curdoc, figure

from bokeh.models.tools import HoverTool, BoxSelectTool

import serial
from serial.tools import list_ports

for port in list_ports.comports():
    if port.description == "Circuit Playground Express":
        cpe_device = port.device

print(cpe_device)
cpe = serial.Serial(cpe_device, timeout=0.05) # zero timeout doesn't catch data

np.random.seed(1)

source = ColumnDataSource(dict(
    period=[0], ax=[0], ay=[0], az=[0]
))

p = figure(plot_height=500, tools="xbox_select,xpan,xbox_zoom,reset")
p.xaxis.major_label_text_font_size = "175%"
p.yaxis.major_label_text_font_size = "175%"

box_select = p.select_one(BoxSelectTool)

p.line(x='period', y='ay', alpha=0.8, line_width=2, color='orange', source=source)
p.scatter(x='period', y='ay', color='orange', source=source)

m1 = Slider(title="Mark 1", value=10, start=0, end=2500, step=1)
m2 = Slider(title="Mark 2", value=2490, start=0, end=2500, step=1)
period_readout = Paragraph(text="Period: ", width=400, height=80,  style={'font-size': '175%'})

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
    line = cpe.readline()
    if(line == b'DATA\n'):
        # New data is available, read it:
        #print("reading data line")
        datastring = cpe.readline()
        data = datastring.split(b' ')[:-1] # strip last newline char
        datafloats = [float(i) for i in data]
        #print(datafloats)

        period = np.linspace(0,2500,500)
        ax = datafloats
        ay = ax
        az = ax
    else:
        # Don't change the data
        # TODO find a cleaner way to handle this
        period = source.data['period']
        ax = source.data['ax']
        ay = ax
        az = ax

    return period, ax, ay, az

def update():
    #print("called update")
    period, ax, ay, az = _get_data()
    source.data = dict(ax=ax, ay=ay, az=az, period=period)


def selection_handler(attrname, old, new):
    selection=source.selected.indices
    sel_data = [source.data['period'][i] for i in selection] # Use time data
    calculated_period = max(sel_data) - min(sel_data)
    #print(calculated_period)
    period_readout.text = "Period: {0:.2f} ms".format(calculated_period)

source.selected.on_change('indices', selection_handler)

#curdoc().add_root(column(row(m1, m2), gridplot([[p]], toolbar_location="left", plot_width=1000)))
curdoc().add_root(column(gridplot([[p]], toolbar_location="left", plot_width=1000)))
curdoc().add_root(row(period_readout, width=1000))
curdoc().add_periodic_callback(update, 500) # This was originally too fast? was 50
# TODO sort out the two callbacks: sliders and periodic. Another way to
# test for new data?

# One option is to set the readline timeout short and just try for new data every 500 ms
# with the periodic update
curdoc().title = "Live Arduino"
