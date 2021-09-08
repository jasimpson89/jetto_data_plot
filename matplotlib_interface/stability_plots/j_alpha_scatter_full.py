import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.animation import FuncAnimation
matplotlib.use('Qt5Agg')

"""
Note that in j_alpha_scatter_plot we have a similar functionality, but this just plots the j-alpha plots for all 
the data 
"""

def main(simulation_data):
    no_cols = 1
    no_rows = 1

    fig, ax = plt.subplots(no_rows, no_cols, sharex=True, sharey=True)

    alfm = []
    cubs = []
    for simulation in simulation_data:
        # jst = simulation['JST']
        # ax.scatter(jst["ALFM"].values,jst["CUBS"].values,c=jst["time"],
        #            marker=simulation.marker)
        if simulation['JST_mishka']:
            jst_mishka = simulation['JST_mishka']
            im = ax.scatter(jst_mishka["ALFM"].values, jst_mishka["CUBS"].values,
                       marker=simulation.marker,c=jst_mishka['time'],s=50, label=simulation.label)


    ax.set_xlabel("Max alpha at unstable time")
    ax.set_ylabel("Max J at unstable time")
    ax.legend()
    fig.colorbar(im, ax=ax)
    ax.set_title("Colorbar just for show, ignore numbers")