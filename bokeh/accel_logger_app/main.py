# based on: https://github.com/bokeh/bokeh/tree/master/examples/app/ohlc
# Waits for block of data over serial to plot in bokeh graph
# use with Arduino accel_logger code on Circuit Playgroud Express
# run with `bokeh serve arduinolive`

import numpy as np

#from bokeh.driving import count
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

box_select = p.select_one(BoxSelectTool)
#box_select.overlay.fill_color = "firebrick"
#box_select.overlay.line_color = None
# TODO get data from box_select (see callbacks further below)

p.line(x='period', y='ay', alpha=0.8, line_width=2, color='orange', source=source)
p.scatter(x='period', y='ay', color='orange', source=source)

m1 = Slider(title="Mark 1", value=10, start=0, end=2500, step=1)
m2 = Slider(title="Mark 2", value=2490, start=0, end=2500, step=1)
period = Paragraph(text="Period: ", width=100, height=80)

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
        # TODO find a cleaner way to handle this
        period = source.data['period']
        ax = source.data['ax']
        ay = ax
        az = ax

    #period = source.data['period'][-1] + 0.1
    #ax, ay, az = np.random.random(),np.random.random(),np.random.random()

    return period, ax, ay, az




#@count()
def update():
    #print("called update")
    period, ax, ay, az = _get_data()

    # new_data = dict(
    #     period=[period],
    #     ax=[ax],
    #     ay=[ay],
    #     az=[az],
    # )

    source.data = dict(ax=ax, ay=ay, az=az, period=period)


def selection_handler(attrname, old, new):
    selectionIndex=source.selected.indices[0]
    print("you have selected the row "+str(selectionIndex))
    # TODO try and make this show the range of time selected

source.selected.on_change('indices', selection_handler)

#curdoc().add_root(column(row(m1, m2), gridplot([[p]], toolbar_location="left", plot_width=1000)))
curdoc().add_root(column(gridplot([[p]], toolbar_location="left", plot_width=1000)))
curdoc().add_root(row(period, width=1000))
curdoc().add_periodic_callback(update, 500) # This was originally too fast? was 50
# TODO sort out the two callbacks: sliders and periodic. Another way to
# test for new data?

# One option is to set the readline timeout short and just try for new data every 500 ms
# with the periodic update
curdoc().title = "Live Arduino"
