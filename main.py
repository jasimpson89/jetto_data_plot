# Std imports
import matplotlib.pyplot as plt

# Package imports

## Data reading
import read_jetto_data.read_data as read_jetto_data
import read_jetto_data.read_input_data as read_input_file
import read_jetto_data.read_data_parallel as read_jetto_data_parallel

## MATPLOTLIB interface
import matplotlib_interface.matplotlib_controller as matplotlib_controller

## Plotly interface
import plotly_interface.plotly_controller as plotly_controller

## Admin
import cmd_argsparse

## BOHEK interface
import bohek_tabs.bohek_controller as bohek_controller




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
    input_file = 'json_input_files/nesep_scan_shows_trend_with_EPED_off_100.json'
    input_file = 'json_input_files/nesep_scan_shows_trend.json'
    input_file = 'json_input_files/10mw_no_helena_namelist.json'
    # input_file = 'json_input_files/pesep_trend_comp_10MW.json'
    opts = cmd_argsparse.parse_opt()
    input_data = read_input_file.read_data(input_file)
    simulation_data = read_jetto_data.read_data(input_data)
    # simulation_data = read_jetto_data_parallel.multi_process(input_data)


    if opts.use_bohek_tabs:
        bohek_controller.bohek_interface(simulation_data,input_data,opts)
    elif opts.plotly:
        plotly_controller.main(simulation_data,input_data,opts)

    else:
        matplotlib_controller.main(simulation_data,opts)
        plt.show()