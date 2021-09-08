# Basic usage

- The program is executed by running the main.py script in the root directory
- Set the parameter 'input_file' in main function of main.py to the path of the input file to be read as the input
- The input files are stored in /json_input_files
- The structure of the input file is as follows:
    - JSON data dictionary
    - At the end of the JSON data, a Mark down section which will be displated on the first tab of the Bohek server
- Please copy test_data_one_case.json for an example and modify that case for your usage

# Hiearchy
```
|- Bohek tabs (web server tabs, activated by -bohek on command line)/
|-- util/ (utilities for plotting tabs)
|-- tab*.py
|
|- data/ (data storage of JSP and JST)
|- json_input_files/ (storage of the input files for the code)
|
|- plotting_routines/ (keep custom plotting routines here when plotting other things not in the JSP/JST calculations etc)
|-- utils/
|--- read_mishkainfo_file.py (reads MISHKA info file
|
|- read_jetto_data/ (reads the jetto data and the (json) input file)
|- analysis routines/ (codes which do work on the data not involved with plotting)
|-- mtanh_fitting/ (fit mtanh to the pedestal)
|-- pedestal_database_reader/ (reads and puts Lorenzo's pedestal database into a pandas datafram)
| 
|- matplotlib_interface/ (when not plotting with bohek use this)
|-- stability_plots/ (plotting routinte for making plot for pedestal stability)
|-- pedestal_database/ (plotting of the pedestal database)
|- matplotlib_controller.py (triggers what to plot in matplotlib)
|
| main.py (runs the script)
| cmd_argparse.py (sets cmd line options)
|README
```