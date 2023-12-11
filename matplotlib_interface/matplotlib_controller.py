# Std imports
import matplotlib.pyplot as plt
import matplotlib

# Package imports
import matplotlib_interface.stability_plots.j_alpha_scatter_plot as j_alpha_scatter
import matplotlib_interface.stability_plots.j_alpha_scatter_full as j_alpha_scatter_full
import matplotlib_interface.stability_plots.gradient_plots as gradient_plots
import matplotlib_interface.pedestal_database.plot_nesep_peped_fits as plot_nesep_peped_fits
import matplotlib_interface.standard_plots.plot_jst_timetraces as plot_jst_timetraces
import matplotlib_interface.standard_plots.plot_jsp_mishka as plot_jsp_timetraces
import matplotlib_interface.pedestal_database.main_plot_fits_and_hrts_data as main_plot_fits_and_hrts_data
import matplotlib_interface.pedestal_database.plot_lorenzo_fits as plot_lorenzo_fits
import matplotlib_interface.europed_plot.europed_plot_controller as europed_plot_controller
import matplotlib_interface.pedestal_database.plot_nesep_peped_fits_for_paper as plot_nesep_peped_fits_for_paper
"""
Control script for the matplotlib interface
- Everything is self contained in each modules. Likely many loops that could be simplified however this makes the code
  much more readable 
"""

def main(simulation_data,opts):
    print('In MATPLOTLIB controller')
    matplotlib.rcParams.update({'font.size': 14})

    # STANDARD CONVERGENCE PLOTS REQUIRED TO JUDGE RUN , profiles + JST data
    plot_jst_timetraces.plot_jst(simulation_data)
    plot_jsp_timetraces.plot_jsp(simulation_data, opts)


    # Make j-alpha scatter plot
    # j_alpha_scatter_full.main(simulation_data)
    # do last because of the way I make a big axis
    # j_alpha_scatter.main(simulation_data)
    # Gradient plots for bootstrap current investigation
    gradient_plots.main(simulation_data)


    # Fits mtanh to profiles and then plots peped v. nesep with experimental data

    if opts.mtanh == True:
        ne_nesep_ax, te_nesep_ax, pe_nesep_ax, te_ped_width_ax, ne_ped_width_ax, mtanh_fits = plot_nesep_peped_fits.main(simulation_data,opts)
        # only save the offset = 0 cases

    else:
        ne_nesep_ax, te_nesep_ax, pe_nesep_ax, te_ped_width_ax, ne_ped_width_ax = plot_nesep_peped_fits.main(
            simulation_data, opts)

    if opts.mtanh == True:
        # basically replicates the above call but produces plots for the paper
        plot_nesep_peped_fits_for_paper.main(simulation_data,mtanh_fits, opts)
    else:
        plot_nesep_peped_fits_for_paper.main(simulation_data,None, opts)



    # This plots the HRTS data for given nesep and then plots the simulation data on the top
    if opts.hrts:
        main_plot_fits_and_hrts_data.main(simulation_data,opts)

    # Plot Lorenzo fits for the peped v. nesep scaling
    if opts.ppf:
        nesep_confined, te_confined, ne_confied  = plot_lorenzo_fits.plot_fits(simulation_data, opts, ne_ped_width_ax, te_ped_width_ax)


    if opts.europed:
        europed_plot_controller.main(simulation_data, [ne_nesep_ax, te_nesep_ax, pe_nesep_ax])

