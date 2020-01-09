# https://stackoverflow.com/questions/46584622/fitting-a-curve-while-updating-a-plot-using-the-bokeh-library-in-python

import pandas as pd
import numpy as np
from bokeh.io import curdoc
from bokeh.layouts import row, widgetbox
from bokeh.models import ColumnDataSource, Select
from bokeh.plotting import figure
from scipy.optimize import curve_fit

def fit_func(xdata, ydata):

    def func(x,a,c):
        return a*(x**2)+a*x+c

    y = func(xdata, 1, 1)
    popt, pcov = curve_fit(func, xdata, ydata)
    new_x = np.arange(0,10,2)
    new_y = func(new_x,*popt)

    return (new_x, new_y)

dc = {'x_val':[0,1,2,3,4], 'Y1':[3.01, 5.10, 6.99, 8.02, 10.81],
     'Y2':[0.99, 3.05, 7.29, 13.41, 20.31]}
df = pd.DataFrame(dc)

source = ColumnDataSource(data={'x': df['x_val'], 'y': df['Y1'], 'y2':df['Y2']})

xf, yf = fit_func(df['x_val'].values, df['Y1'].values)
source_f = ColumnDataSource(data={'x': xf, 'y': yf})

plot = figure(x_axis_label = 'x', y_axis_label = 'f(x)')
plot.circle('x', 'y', source=source)
plot.line('x', 'y', source=source_f)

def update_plot(attr, old, new):
        y = y_select.value
        new_data = {'x': df['x_val'], 'y': df[y]}
        source.data = new_data

        answ = fit_func(df['x_val'].values, df[y].values)
        new_fit = {'x':answ[0], 'y':answ[1]}
        source_f.data = new_fit

y_select = Select(options=['Y1', 'Y2'],value='Y1',title='y-axis data')
y_select.on_change('value', update_plot)

layout = row(widgetbox(y_select), plot)
curdoc().add_root(layout)
