# Std imports
import matplotlib.pyplot as plt

# Package imports

## Data reading
import read_jetto_data.read_data as read_jetto_data
import read_jetto_data.read_input_data as read_input_file
import read_jetto_data.read_data_parallel as read_jetto_data_parallel
import json_from_CLI 
## MATPLOTLIB interface
import matplotlib_interface.matplotlib_controller as matplotlib_controller



## Admin
import cmd_argsparse





if __name__ == '__main__':

    # Load input data from JSON file
    # input_file = 'json_input_files/luca_rerun_nesep_1_3_mode_analysis.json'
    # input_file = 'json_input_files/luca_rerun_nesep_1_3_analysis.json'
    # input_file = 'json_input_files/luca_rerun_nesep_1_3.json'
    # input_file = 'json_input_files/luca_rerun.json'
    # input_file = 'json_input_files/luca_rerun.json'
    # input_file = 'json_input_files/luca_rerun_E2D_BC_only.json'
    # input_file = 'json_input_files/nesep_scan_shows_trend.json'
    # input_file = 'json_input_files/temp_input.json'
    # input_file = 'json_input_files/comp_frantic_and_eirene.json'
    # input_file = 'json_input_files/luca_rerun_REMOVED_EDGE_SOURCE.json'
    # input_file = 'json_input_files/luca_rerun_REMOVED_EDGE_SOURCE_COMP.json'
    # input_file = 'json_input_files/luca_rerun_REMOVED_EDGE_SOURCE_COMP_NESEP_3_ONLY.json'
    # input_file = 'json_input_files/nesep_scan_shows_trend_with_EPED_off_100.json'
    # input_file = 'json_input_files/nesep_scan_shows_trend.json'
    # input_file = 'json_input_files/10mw_no_helena_namelist.json'
    # input_file = 'json_input_files/work_loc/test_heimdall.json'
    # input_file = 'json_input_files/pesep_trend_comp_10MW.json'
    # input_file = 'json_input_files/work_loc/nesep_1_fixed_width_tessep_100.json'
    # input_file = 'json_input_files/work_loc/nesep_fixed_width_tesep_100.json'
    # input_file = 'json_input_files/work_loc/nesep_fixed_width_tesep_E2D.json'
    # input_file = 'json_input_files/work_loc/nesep_EPED_tesep_100.json'
    # input_file = 'json_input_files/work_loc/nesep_EPED_tesep_E2D.json'
    # input_file = 'json_input_files/work_loc/nesep_EPED_tesep_E2D_started_nesep_1_5.json'
    # input_file = 'json_input_files/work_loc/test_particle_content_R_1.json'
    # input_file = 'json_input_files/work_loc/test_heimdall.json'
    # input_file = 'json_input_files/work_loc/nesep_fixed_width_scan_D_Chi_scan_tesep_100.json'
    input_file = 'json_input_files/work_loc/nesep_fixed_width_scan_tesep_100.json'
    # input_file = 'json_input_files/work_loc/nesep_fixed_width_scan_tesep_100_comp_nesep_1_4.json'
    # input_file = 'json_input_files/work_loc/nesep_fixed_width_scan_D_Chi_scan_tesep_100_low_nesep.json'
    # input_file = 'json_input_files/work_loc/nesep_fixed_width_scan_D_Chi_scan_tesep_100_high_nesep.json'
    #input_file = 'json_input_files/work_loc/nesep_fixed_width_transport_edge_scan.json'
    # input_file = 'json_input_files/work_loc/additional_transport_comp_0.98_1.0.json'
    # input_file = 'json_input_files/work_loc/grad_n_scan.json'
    # input_file = 'json_input_files/work_loc/gaussian_transport_scan_with_gradn.json'
    # input_file = 'json_input_files/work_loc/gaussian_transport_scan_ne_width_1.5.json'
    # input_file = 'json_input_files/work_loc/gaussian_transport_scan_ne_width_2.5.json'
    # input_file = 'json_input_files/work_loc/gaussian_transport_scan_ne_width_fixed_nesep_scan.json'
    # input_file = 'json_input_files/work_loc/gaussian_transport_scan_grad_n_scan.json'
    # input_file = 'json_input_files/work_loc/gaussian_transport_scan_lorenzo_scaling.json'
#




    opts = cmd_argsparse.parse_opt()

    if opts.jetto_runs is not None:
        # The runs are taken from the command line and not taken from the JSON file
        # labels are an optional extra when passed on the command line
        print('USING COMMAND LINE INPUT')
        input_data = json_from_CLI.create_json_array_from_cli(opts.jetto_runs,opts.labels)
        simulation_data = read_jetto_data.read_data(input_data)

    else:
        # This is stanadard way of reading the json file 
        input_data = read_input_file.read_data(input_file)
        simulation_data = read_jetto_data.read_data(input_data)
    # simulation_data = read_jetto_data_parallel.multi_process(input_data)


    if opts.use_bohek_tabs:
        ## BOHEK interface
        import bohek_tabs.bohek_controller as bohek_controller
        bohek_controller.bohek_interface(simulation_data,input_data,opts)
    elif opts.plotly:
        ## Plotly interface
        import plotly_interface.plotly_controller as plotly_controller
        plotly_controller.main(simulation_data,input_data,opts)

    else:
        matplotlib_controller.main(simulation_data,opts)
        plt.show()
