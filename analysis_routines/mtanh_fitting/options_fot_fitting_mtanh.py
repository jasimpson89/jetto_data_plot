import json
def fitting_options(position,neped,width,slope,parameter_name):

    with open("analysis_routines/mtanh_fitting/fitting_options.json",'r') as read_file:
        fitting_parms = json.load(read_file)

#     choose the fitting parameters wanted

    chosen_fit_parms = fitting_parms[parameter_name]
#     update with fit things it needs to know

    chosen_fit_parms["inital_guess"]["position"] = position
    chosen_fit_parms["inital_guess"]["height"] = neped

#     Upate bounds
    chosen_fit_parms["bounds"]["position_min"] = float(chosen_fit_parms["bounds"]["position_min"])*position
    chosen_fit_parms["bounds"]["position_max"] = float(chosen_fit_parms["bounds"]["position_max"])*position
    chosen_fit_parms["bounds"]["height_min"] = float(chosen_fit_parms["bounds"]["height_min"])*neped
    chosen_fit_parms["bounds"]["height_max"] = float(chosen_fit_parms["bounds"]["height_max"])*neped
    chosen_fit_parms["bounds"]["width_min"] = float(chosen_fit_parms["bounds"]["width_min"]) * width
    chosen_fit_parms["bounds"]["width_max"] = float(chosen_fit_parms["bounds"]["width_max"]) * width
    chosen_fit_parms["bounds"]["slope_min"] = float(chosen_fit_parms["bounds"]["slope_min"]) * slope
    chosen_fit_parms["bounds"]["slope_max"] = float(chosen_fit_parms["bounds"]["slope_max"]) * slope

    return chosen_fit_parms



