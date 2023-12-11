"""
Example of a json file array format 
}
"runs": {
     "run0": {
        "globals": {
        "run_dir": "/common/cmg/jsimpson/jetto/runs/runluca_restart_fixed_width_neped_5_e19_t_sep_100_width_1.5cm_guassian_transport_1e4_nesep_4/",
          "read_jst": "True"
        },
        "plot_options": {
          "label": "nesep=4 te=1.5cm ne=1.5cm 1e3cm2",
          "color": "k",
          "marker_color": "w",
          "linestyle": "-",
          "marker": "o"
        }
      }
}
"""
def create_json_array_from_cli(simulation_list,labels):
  """
  This creates the json data but just based on the command line input

  It ouputs a json dictionary in the same format as the json input files to be consistient which can then be used in the usual parsing routines
  """

  # Set up the date the JSON file needs
  # TODO put this in a config file or something
  runs = {}
  color = ['r', 'g', 'b', 'k', 'c', 'y', 'm','darkmagenta', 'slategray','hotpink']
  marker = ['o']*len(color)

  linestyle = ['-']*len(color)
  runs['runs'] = {}
  for i in range(0,len(simulation_list)):
    run_name = "run"+str(i)
    # run_name = "run"
    # globals
    
    runs['runs'][run_name] = {}
    runs['runs'][run_name]["globals"] = {}
    # TODO put this in a config file and make a command line swtich to provide a full path
    common_run_dir = '/common/cmg/jsimpson/jetto/runs/'
    runs['runs'][run_name]["globals"]["run_dir"] = common_run_dir+simulation_list[i]
    runs['runs'][run_name]["globals"]["read_jst"] = 'True'

    # Plot options
    runs['runs'][run_name]["plot_options"] = {}

    if labels is not None:
        runs['runs'][run_name]["plot_options"]["label"] = labels[i]
    else:        
        runs['runs'][run_name]["plot_options"]["label"] = simulation_list[i]
    
    runs['runs'][run_name]["plot_options"]["color"] = color[i]
    runs['runs'][run_name]["plot_options"]["marker_color"] = color[i]
    runs['runs'][run_name]["plot_options"]["linestyle"] = linestyle[i]
    runs['runs'][run_name]["plot_options"]["marker"] = marker[i]

  return runs

# if __name__ == "__main__":
#     runs = create_json_array_from_cli(['test1','test2'])
#     print(runs)