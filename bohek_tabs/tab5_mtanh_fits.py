# Package imports
import bohek_tabs.tab_utils.plot_tab_constructor as hvplot_tab_constructor
import bohek_tabs.plotting_routines.stability_plots as stability_plots
import analysis_routines.mtanh_fitting.mtanh_interface as mtanh_interface
# std imports
import panel as pn
pn.extension()
import pandas as pd
import hvplot.pandas
def fit_mtanh(simulation_data,opts):

    # these are used to make a pandas dataframe at the end of plotting
    density_fit = {}
    temperature_fit = {}

    # plot object list
    temp_plots = []
    density_plots = []

    for simulation in simulation_data:
        density_fit_profile = {}
        temperature_fit_profile = {}
        if "JST_mishka" in simulation:
            # Make mtanh fits
            # pythonistas say i shoudl use try except here rather than hasatttr its slower
            if hasattr(simulation, "mtanh_fit_time"):
                # time can be specified in the JSON file
                time = simulation.mtanh_fit_time

            elif simulation["JST_mishka"]:
                ## select last unstable time
                jst = simulation["JST_mishka"].isel(time=-1)
                time = float(jst.coords["time"])

            # temperature data
            teped, deltate, teped_pos_offset, chi_square, fit_data_te, r_end_time_te, raw_data_te = \
                mtanh_interface.fit_one_profile(simulation, opts, "TE", time)
            temperature_fit['height'] = teped
            temperature_fit['width'] = deltate

            temperature_fit_profile['x_axis'] = r_end_time_te
            temperature_fit_profile['profile'] = fit_data_te
            temperature_fit_profile['raw_data'] = raw_data_te
            temp_df = pd.DataFrame(temperature_fit_profile)
            # NOTE THE LIMITS, HVPLOT FOR some reason uses the same limts as density plot?
            # shared_axes=False fixed this.
            dt = temp_df.hvplot(x='x_axis', y=['profile', 'raw_data'],
                                     label=simulation.label,shared_axes=False)
            temp_plots.append(dt)


            # density data
            neped, deltane, neped_pos_offset, chi_square, fit_data, r_end_time, raw_data= \
            mtanh_interface.fit_one_profile(simulation, opts, "NE", time)
            density_fit['height']=neped
            density_fit['width']=deltane

            density_fit_profile['x_axis'] = r_end_time
            density_fit_profile['profile'] = fit_data
            density_fit_profile['raw_data'] = raw_data
            density_df  = pd.DataFrame(density_fit_profile)
            dp = density_df.hvplot(x='x_axis',y=['profile','raw_data'],label=simulation.label,shared_axes=False)
            density_plots.append(dp)



    # build plots into tabs
        if density_plots:  # make sure its not empty, v. unlikely not also have temp_plot
            tabs = pn.Tabs()
            tab1 = hvplot_tab_constructor.tab_constructor(temp_plots, 3)
            tabs.append(('temperature MTANH FIT', tab1))
            tab = hvplot_tab_constructor.tab_constructor(density_plots, 3)
            tabs.append(('density MTANH FIT', tab))

            return tabs


