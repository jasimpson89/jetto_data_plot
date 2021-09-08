# Std imports
import matplotlib.pyplot as plt
import matplotlib

# Package imports
import matplotlib_interface.stability_plots.j_alpha_scatter_plot as j_alpha_scatter
import matplotlib_interface.stability_plots.j_alpha_scatter_full as j_alpha_scatter_full
import matplotlib_interface.stability_plots.gradient_plots as gradient_plots
import matplotlib_interface.pedestal_database.plot_nesep_peped_fits as plot_nesep_peped_fits
"""
Control script for the matplotlib interface
- Everything is self contained in each modules. Likely many loops that could be simplified however this makes the code
  much more readable 
"""

def main(simulation_data,opts):
    print('In MATPLOTLIB controller')
    matplotlib.rcParams.update({'font.size': 14})

    # Make j-alpha scatter plot
    j_alpha_scatter_full.main(simulation_data)
    # do last because of the way I make a big axis
    j_alpha_scatter.main(simulation_data)
    # Gradient plots for bootstrap current investigation
    gradient_plots.main(simulation_data)

    # TODO get this from command line
    fit_mtanh=True
    if fit_mtanh == True:
        # Fits mtanh to profiles and then plots peped v. nesep with experimental data
        plot_nesep_peped_fits.main(simulation_data,opts)