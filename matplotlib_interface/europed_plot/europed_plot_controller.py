import matplotlib_interface.europed_plot.plot_europed_runs as plot_europed_runs
import matplotlib_interface.europed_plot.read_europed_data as read_europed_data
def main(simulations, ped_top_ax):

    te_ax, ne_ax, pre_ax, ti_ax = plot_europed_runs.plot_jsp(simulations)

    read_europed_data.read_plot_europed_data([ne_ax, te_ax], ped_top_ax)