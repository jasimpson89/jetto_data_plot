# Std imports
import os
import distutils.util
import multiprocessing.pool

# Dependcies
from jetto_tools.classes import JETTO

# Pkg imports
import read_jetto_data.read_mishkainfo_file as read_mishka
"""
This module reads the jetto in a loop, prodivided to it

Then uses the Xarray attrs method to store extra data requited for plotting
"""

def interpolate_mishka_data(path,load_jst,simulation):
    file_path = path + '/MISHKAinstabilities.info'
    if os.path.isfile(file_path):
        mishka_data = read_mishka.read_info_file(path)

        jsp = simulation['JSP']
        # interpolate mishka_data onto jst time axis
        jsp_on_mishka_time_axis = jsp.interp(time=mishka_data["time"])
        jsp_on_mishka_time_axis["unstable_mode"] = mishka_data
        # Now merge into the JST profile
        jsp = jsp.merge(jsp_on_mishka_time_axis)
        simulation['JSP'] = jsp
        simulation['JSP_mishka'] = jsp_on_mishka_time_axis

    else:
        # file doesn't exist
        return None

    if load_jst: # interpolate MISHKA data onto JST
        jst = simulation['JST']
        # interpolate mishka_data onto jst time axis
        jst_on_mishka_time_axis = jst.interp(time=mishka_data["time"])
        jst_on_mishka_time_axis["unstable_mode"] = mishka_data
        # Now merge into the JST profile
        jst = jst.merge(jst_on_mishka_time_axis)
        simulation['JST'] = jst
        simulation['JST_mishka'] = jst_on_mishka_time_axis
        return simulation


def set_up_data_store(jetto_data, plot_label, color, marker,load_jst ,run_path,marker_edge_color='w'):

    jetto_data.label = plot_label
    jetto_data.load_jst = load_jst
    jetto_data.run_dir = run_path
    jetto_data.marker = marker
    jetto_data.color = color
    jetto_data.marker_edge_color = marker_edge_color

    return jetto_data


def read_data(run):
    """
    :param input_data - data read in from json file as input
    from JSON only GLOBALS and PLOT_DATA is used
    """


    # path to simulation

    run_path = run["globals"]["run_dir"]
    load = bool(distutils.util.strtobool(run["globals"]["read_jst"]))

    # LOAD JETTO DATA FROM CLASS
    jetto_run = JETTO(run_path, load_jst=load)

    # TODO - remove this when integrated into JETTO-pythontools
    # interpolate mishka data on JST or JSP time basis, and also keep separate
    sim_temp = interpolate_mishka_data(run_path, load, jetto_run)
    if sim_temp is not None:  # handle error
        jetto_run = sim_temp

    #################################################################
    # unpack all the REST of the json data for plotting
    # converting to Boolean is non trival in python see - https://stackoverflow.com/questions/715417/converting-from-a-string-to-boolean-in-python
    label = run["plot_options"]["label"]
    color = run["plot_options"]["color"]
    marker_color = run["plot_options"]["marker_color"]
    linestyle = run["plot_options"]["linestyle"]
    marker = run["plot_options"]["marker"]

    # finished unpacking JSON

    # Load the JETTO data
    jetto_data_plotting_dictionary = set_up_data_store(jetto_run, label,
                                                       color, marker, load,run_path, marker_edge_color='w')





    return jetto_data_plotting_dictionary

def multi_process(input_data):
    """

    :param input_data: JSON structure read from input file
    :return: JETTO class object and associated plotting details
    """

    # Set up multiporcessing tool
    a_pool = multiprocessing.Pool()
    runs = []


    # For mulitprocessing to work I THINK, we need an interable single depth list of each simulation which is
    # defined in the JSON structure. The runs list builds this. It will look like
    # run[0] - data for simulation 1, path etc
    # run[1] - data for simulation 2, path etc

    for run_name in input_data["runs"].keys():
        run = input_data["runs"][run_name]
        runs.append(run)

    # call multiprocess and map the read_data function to the runs list
    simulation_store =a_pool.map(read_data, runs)
    return simulation_store
