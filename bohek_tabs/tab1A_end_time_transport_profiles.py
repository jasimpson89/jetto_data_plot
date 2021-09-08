import xarray as xr
import panel as pn
pn.extension()
import bohek_tabs.tab_utils.plot_tab_constructor as hvplot_tab_constructor


def plot_tab(simulation_data):
    """
    :param - simulation_data - array of JETTO classes read from JSP and JST etc
    """
    # Select the parameters to be plotted in this array
    jsp_plot_vars = ['XE','XE1','XE2','XE3','XI','XI1','XI2','XI3','D1','DNCI']

    plots_container = []

    # Make plots for all the JETTO class object
    for simulation in simulation_data:
        if 'JSP_mishka' in simulation:
            print('END TIME is MISHKA LAST PROFILE')
            simulation_plot = hvplot_tab_constructor.plot_constructor_jsp(simulation['JSP_mishka'].isel(time=-1)
                                                                          , simulation, jsp_plot_vars)
        else:
            # Make plots for each simulation, note simulation is passed in for it meta plotting data
            simulation_plot = hvplot_tab_constructor.plot_constructor_jsp(simulation['JSP'].isel(time=-1)
                                                                      ,simulation,jsp_plot_vars)
        plots_container.append(simulation_plot)

    # We now need to overplot all plots we have made
    no_columns = 2
    overplot_container = hvplot_tab_constructor.overplot(plots_container)

    panel = hvplot_tab_constructor.tab_constructor(overplot_container,no_columns)

    return panel