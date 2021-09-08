## BOHEK TABS
import bohek_tabs.tab1_end_time_profiles as tab1_end_time
import bohek_tabs.tab1A_end_time_transport_profiles as tab1_transport_end_times
import bohek_tabs.tab2_time_evolution_profiles as tab2_time_evolution
import bohek_tabs.tab3_jst_pedestal_data as tab3_jst_pedestal
import bohek_tabs.tab0_talking_points_page as tab_talking_points
import bohek_tabs.tab4_mishka_stability as tab_stability_data


## Std imports
import panel as pn
pn.extension()
def bohek_interface(simulation_data,input_data,opts):
    print('Starting BOHEK server')
    tab_talking_points_text = tab_talking_points.markdown_talking_points(input_data["notes"])


    time_evolve_tab = False
    if time_evolve_tab == True:
        tab1_panel = tab2_time_evolution.plot_tab(simulation_data)
    else:
        # STANDARD PLOTS end time only
        tab1_panel = tab1_end_time.plot_tab(simulation_data)

    tab_transport = tab1_transport_end_times.plot_tab(simulation_data)
    tabs = pn.Tabs(('Talking points', tab_talking_points_text),
                   ('Profile', tab1_panel),
                   ('Transport profiles', tab_transport))

    # Set up talking points
    # Make tabs
    tab3_panel = tab3_jst_pedestal.plot_tab(simulation_data)
    if tab3_panel is not None:
        # TODO simplify this so tabs an easily toggled on an off
        tabs.append(('Pedestal JST Data', tab3_panel))


    # CUSTOM PLOTTING and append tabs
    tab_stability = tab_stability_data.stab_plots(simulation_data)
    if tab_stability is not None:
        tabs.append(('Stability', tab_stability))

    if opts.bfgs_flag:
        import bohek_tabs.tab5_mtanh_fits as tab_mtanh
        tab_mtanh_fit = tab_mtanh.fit_mtanh(simulation_data,opts)
        if tab_mtanh_fit is not None:
            tabs.append(('MTANH fits', tab_mtanh_fit))





    server = tabs.show(title='JETTO DATA BOARD', threaded=True)

