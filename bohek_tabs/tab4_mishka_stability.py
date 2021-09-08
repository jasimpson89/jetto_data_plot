# Package imports
import bohek_tabs.tab_utils.plot_tab_constructor as hvplot_tab_constructor
import bohek_tabs.plotting_routines.stability_plots as stability_plots

# std imports
from functools import reduce
import panel as pn
pn.extension()


def stab_plots(simulation_data):
    # Add here all the plots we want for stability plotting.
    # these don't need to be as eleganlty created as the standard JSP and JST plots

    # Make j-alpha plots but we need all data in the same dataframe

    # Make these plots separetly for each jetto run
    plots = []
    t1p = []
    t2p = []
    t3p = []


    for simulation in simulation_data:
        if "JST_mishka" in simulation:
            alpha, j_bootstrap = stability_plots.make_j_alpha_plot(simulation, simulation['JST_mishka'])

            plots.append(alpha)
            plots.append(j_bootstrap)

            t1,t2,t3 = stability_plots.pressure_gradient(simulation)

            t1p.append(t1)
            t2p.append(t2)
            t3p.append(t3)
        # Make pressure gradient plots if mtanh fits




    if plots: #make sure its not empty
        tabs = pn.Tabs()
        tab = hvplot_tab_constructor.tab_constructor(plots,1)
        tabs.append(('JST stability', tab))


        row = pn.Row()
        t1 = reduce(lambda x, y: x * y, t1p)
        t1.opts(shared_axes=False)

        row.append(t1)
        t2 = reduce(lambda x, y: x * y, t2p)
        t2.opts(shared_axes=False)
        row.append(t2)

        t3 = reduce(lambda x, y: x * y, t3p)
        t3.opts(shared_axes=False)
        row.append(t3)
        cols=pn.Column(*row)
        tab2=pn.panel(cols)
        tabs.append(('Gradient NOT mtanh', tab2))


        return tabs
    else:
        return None

