import numpy as np
import matplotlib.pyplot as plt

def setup_profile_plots():

    fig,ax = plot.subplots(nrows=3, ncols=2)

    ax[0,0].set_xlable('nesep')

def plot_jsp(simulations):

    for simulation in simulations:
        jsp = simulation['JSP_mishka']
