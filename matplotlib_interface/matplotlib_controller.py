# Std imports
import matplotlib.pyplot as plt
import matplotlib

# Package imports
import matplotlib_interface.stability_plots.j_alpha_scatter_plot as j_alpha_scatter
import matplotlib_interface.stability_plots.j_alpha_scatter_full as j_alpha_scatter_full
import matplotlib_interface.stability_plots.gradient_plots as gradient_plots
import matplotlib_interface.pedestal_database.plot_nesep_peped_fits as plot_nesep_peped_fits
import matplotlib_interface.standard_plots.plot_jst_timetraces as plot_jst_timetraces
"""
Control script for the matplotlib interface
- Everything is self contained in each modules. Likely many loops that could be simplified however this makes the code
  much more readable 
"""

def main(simulation_data,opts):
    print('In MATPLOTLIB controller')
    matplotlib.rcParams.update({'font.size': 14})

    # STANDARD CONVERGENCE PLOTS REQUIRED TO JUDGE RUN
    plot_jst_timetraces.plot_jst(simulation_data)


    # Make j-alpha scatter plot
    j_alpha_scatter_full.main(simulation_data)
    # do last because of the way I make a big axis
    j_alpha_scatter.main(simulation_data)
    # Gradient plots for bootstrap current investigation
    gradient_plots.main(simulation_data)


    # Fits mtanh to profiles and then plots peped v. nesep with experimental data
    plot_nesep_peped_fits.main(simulation_data,opts)