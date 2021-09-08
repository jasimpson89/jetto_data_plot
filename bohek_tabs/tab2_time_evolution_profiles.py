import xarray as xr
import numpy as np
import panel as pn
pn.extension()
import bohek_tabs.tab_utils.plot_tab_constructor as hvplot_tab_constructor


def plot_tab(simulation_data):
    """
    :param - simulation_data - array of JETTO classes read from JSP and JST etc
    """
    # Select the parameters to be plotted in this array
    #NOTE - if you put a list within the list it plot on the same plot e..g. ['JZ','JZBS'] will plot two lines on the same plot for the current
    jsp_plot_vars = ['TE','NE','TI','PRE',['JZ','JZBS']]

    plots_container = []
    quick_plot = False # uses alot less time slices
    # Make plots for all the JETTO class object
    for simulation in simulation_data:
        # Make plots for each simulation, note simulation is passed in for it meta plotting data
        if quick_plot == True:
            time_evo_step = 20
            time_evolution_sameple = np.linspace((simulation['JSP'].coords['time'][0]).values, (simulation['JSP'].coords['time'][-1]).values,
                                                 num=time_evo_step)
            simulation_plot = hvplot_tab_constructor.plot_constructor_jsp(simulation['JSP'].sel(time=time_evolution_sameple,method='nearest')
                                                                          ,simulation,jsp_plot_vars)

        simulation_plot = hvplot_tab_constructor.plot_constructor_jsp(simulation['JSP'], simulation, jsp_plot_vars)

        plots_container.append(simulation_plot)

    # We now need to overplot all plots we have made
    no_columns = 2
    overplot_container = hvplot_tab_constructor.overplot(plots_container)

    panel = hvplot_tab_constructor.tab_constructor(overplot_container,no_columns)

    return panel