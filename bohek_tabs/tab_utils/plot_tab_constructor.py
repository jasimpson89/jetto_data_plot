import xarray as xr
import hvplot.xarray
import holoviews as hv
from functools import reduce
import panel as pn
# hv.extension('bokeh')
pn.extension()

"""
Description:

- This module takes a JSP or JST file and plots the output onto a panel ready to be used on tab
- Any tab which wants a grid style layout of plots which are interactive or not should use this module
 
"""

def plot_constructor_jst(jst,jetto_class,plot_vars,):
    """
    :param sim_data: list which contains JETTO class
    :param plot_vars: variables in the JETTO['JST'] which want to be plotted
    :return:
    """
    plots = []
    for jst_var in plot_vars:
        # check if the time axis is bigger than 1 for we can make a dynamic plot
        if type(jst_var) in [list]:
            # make initial plot then add on top
            t = jst[jst_var[0]].hvplot.line(label=jetto_class.label, dynamic=False,
                                   width=400, height=300,line_color=jetto_class.color)
            for x in jst_var[1:]:
                # TODO this can be improved
                # Read the rest of the array
                t = jst[x].hvplot.line(label=jetto_class.label,dynamic=False,
                            width=400,height=300,line_dash='dotted',line_color=jetto_class.color)*t
        else:
            t = jst[jst_var].hvplot.line(label=jetto_class.label, dynamic=False,
                                            width=400, height=300,line_color=jetto_class.color)

        plots.append(t)

    return plots

def plot_constructor_jsp(jsp,jetto_class,plot_vars,):
    """
    :param sim_data: list which contains JETTO class
    :param plot_vars: variables in the JETTO['JSP'] which want to be plotted
    :return:
    """
    plots = []
    for jsp_var in plot_vars:
        # check if the time axis is bigger than 1 for we can make a dynamic plot
        if jsp['time'].size > 1:
            if type(jsp_var) in [list]:
                # make initial plot then add on top
                t = jsp[jsp_var[0]].hvplot.line(groupby='time',label=jetto_class.label, dynamic=False,
                                                width=400, height=300,line_color=jetto_class.color)
                for x in jsp_var[1:]:
                    # TODO this can be improved
                    # Read the rest of the array
                    t = jsp[x].hvplot.line(groupby='time',label=jetto_class.label, dynamic=False,
                                           width=400, height=300, line_dash='dotted',line_color=jetto_class.color) * t
            else:
                t = jsp.hvplot.line(groupby='time',x='R',y=jsp_var, label=jetto_class.label,dynamic=True,
                                width=400,height=300,line_color=jetto_class.color)
        else:
            if type(jsp_var) in [list]:
                # make initial plot then add on top
                t = jsp[jsp_var[0]].hvplot.line(label=jetto_class.label, dynamic=False,
                                       width=400, height=300,line_color=jetto_class.color)
                for x in jsp_var[1:]:
                    # TODO this can be improved
                    # Read the rest of the array
                    t = jsp[x].hvplot.line(label=jetto_class.label,dynamic=False,
                                width=400,height=300,line_dash='dotted',line_color=jetto_class.color)*t
            else:
                t = jsp[jsp_var].hvplot.line(label=jetto_class.label, dynamic=False,
                                                width=400, height=300,line_color=jetto_class.color)

        plots.append(t)

    return plots
def overplot(plots_container):
    """
    THIS DOES NOT WORK FOR NDOVERLAYS generated by subplots

    :param plots_container:
    :return:
    """
    overplot_container = []

    #NOTE each element of plots_container should be the same length. i.e. jsp_plot_vars
    # TODO rewrite this loop it can be better
    for j in range(0,len(plots_container[0])): # looping over the jsp_plot_vars
        single_plot_container = []
        for i in range(0,len(plots_container)): # looping over the jsp files which have been read
                single_plot_container.append(plots_container[i][j])

        single_overplot = reduce(lambda x, y: x * y, single_plot_container)
        overplot_container.append(single_overplot)

    return overplot_container

def tab_constructor(plots,no_columns):
    """
    THIS DOESNT WORK FOR NDOVERLAYS GENERATED BY SUBPLOTS
    :param plots:
    :param no_columns:
    :return:
    """
    number_of_plots = len(plots)
    rows = []

    # number of rows filled completely
    number_plots_for_rows = int(number_of_plots/no_columns)

    # how many left we need to put on the last column
    reminder_plots = number_of_plots-(number_plots_for_rows*no_columns)

    for i in range(0, number_plots_for_rows*no_columns, no_columns):
        row = pn.Row()
        for j in range(i, i + no_columns):
            row.append(plots[j])
        rows.append(row)


    # sort out the remaining plots (this should ways be less than the no_columns

    row = pn.Row()
    for k in range(number_of_plots-reminder_plots,number_of_plots):
        # should only ever set up the last column
        row.append(plots[k])

    rows.append(row)

    plot_panel = pn.Column(*rows)

    panel = pn.panel(plot_panel)
    return panel