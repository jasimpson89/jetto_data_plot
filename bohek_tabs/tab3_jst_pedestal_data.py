import xarray as xr
import panel as pn
pn.extension()
import bohek_tabs.tab_utils.plot_tab_constructor as hvplot_tab_constructor


def plot_tab(simulation_data):
    """
    :param - simulation_data - array of JETTO classes read from JSP and JST etc
    """
    # Select the parameters to be plotted in this array
    jst_plot_vars = ['NEBA','TEBA','TIBA','CUBS','ALFM','ALFJ']

    plots_container = []

    # Make plots for all the JETTO class object
    for simulation in simulation_data:
        if simulation.load_jst == True: # make sure data is loaded
            # Make plots for each simulation, note simulation is passed in for it meta plotting data
            simulation_plot = hvplot_tab_constructor.plot_constructor_jst(simulation['JST'],simulation,jst_plot_vars)
            plots_container.append(simulation_plot)

    if plots_container: # if plot_container is an empty list don't do any of this stuff
        # Error handling incase all runs don't have JST
        # We now need to overplot all plots we have made
        no_columns = 2
        overplot_container = hvplot_tab_constructor.overplot(plots_container)

        panel = hvplot_tab_constructor.tab_constructor(overplot_container,no_columns)

        return panel
    else:
        return None