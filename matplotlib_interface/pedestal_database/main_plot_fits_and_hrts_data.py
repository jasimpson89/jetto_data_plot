import matplotlib.pyplot as plt
import analysis_routines.pedestal_database_reader.read_plot_samuli_data as read_exp_ped_data
import analysis_routines.read_experimental_data.read_hrts.read_hrts_data as read_hrts


def setup_plot_axis():
    # use this routine configure the axes you need and the details
    fig_profiles, [te_ax,ne_ax] = plt.subplots(ncols=2,nrows=1)
    
    te_ax.set_xlabel(r'$\psi_n$')
    te_ax.set_ylabel(r'$T_e eV$')
    
    ne_ax.set_xlabel(r'$\psi_n$')
    ne_ax.set_ylabel(r'$n_e m^{-3}$')

    return fig_profiles, te_ax, ne_ax


def main(simulations):
    # This routine calls the various routines to plots fits, hrts data and simulation data 

    # get axes for plotting
    fig_profiles, te_ax, ne_ax = setup_plot_axis()
    # These dataframe consisit of the data from the pedestal database
    # pe_nesep_exp_stability_filter_df is the merging of the other dataframes on shot, and so has the stbaility data from samuli and the data frome lorenzo
    pe_nesep_exp_df,stability_df,pe_nesep_exp_stability_filter_df = read_exp_ped_data.main()
    

    # filter for the nesep you want
    nesep=2
    multiplier = 0.2
    requested_nesep_higher = 2.2#nesep*(1+multiplier)
    requested_nesep_lower = 1.8#nesep*(1-multiplier)    
    
    # Filter the neseps requested
    df_nesep_request = pe_nesep_exp_stability_filter_df[(pe_nesep_exp_stability_filter_df.nesep < requested_nesep_higher) & (pe_nesep_exp_stability_filter_df.nesep > requested_nesep_lower)]
    
    df_nesep_request = pe_nesep_exp_stability_filter_df

    for shot,t1,t2 in zip(df_nesep_request.shot, df_nesep_request.t1,df_nesep_request.t2):

        # get HRTS data
        print(shot)
        print(t1)
        # shifted_x_axis, shifted_ne_profile,shifted_te_profile, shifted_ne_error, shifted_te_error

        te, ne, error_on_te, error_on_ne, psi = read_hrts.read_data(shot,t1,t2) 
        te_ax.plot(psi,te, marker='*')
        ne_ax.plot(psi,ne, marker='*')



    # Set up main loop to read the data 

    for simulation in simulations:
        jsp = simulation['JSP_mishka']
        jsp = jsp.isel(time=-1)
        te_ax.plot(jsp['XPSI'],jsp['TE'],linestyle=simulation.linestyle,color=simulation.color,linewidth=5,label=simulation.label)
        ne_ax.plot(jsp['XPSI'],jsp['NE'],linestyle=simulation.linestyle,color=simulation.color,linewidth=5,label=simulation.label)
