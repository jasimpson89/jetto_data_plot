from numpy import  tanh, abs, linspace, exp
from scipy.optimize import brute # produce good starting guess from bounds
from scipy.optimize import fmin_l_bfgs_b # optimise starting guess from bounds
from scipy.optimize import curve_fit # used to produce covariance matrix from previous methods in scipy
import matplotlib.pyplot as plt
import numpy as np
import analysis_routines.mtanh_fitting.options_fot_fitting_mtanh as options_fot_fitting_mtanh


class fit_1_neped_class:

    def __init__(self, simulation_profile, x_axis,bounds=None):

        self.simulation_profile = simulation_profile
        self.x_axis = x_axis
        self.bounds = bounds

    def cost(self, theta):
        prediction = self.prediction(theta)

        return np.square(self.simulation_profile - prediction).sum()

    def chi_squared(self, theta, normalise=True):
        """
        You want to minimise chi squared to optomise the fit

        :param theta:
        :return:
        """
        prediction = self.prediction(theta)
        normalised_residuals = (self.simulation_profile - prediction) / self.simulation_profile
        if not normalise:
            return np.square(normalised_residuals)
        chi_squared = np.square(normalised_residuals).sum()
        normalised_chi_squared = chi_squared / len(self.simulation_profile)

        return normalised_chi_squared

    def prediction(self, theta):
        prediction_varriables = [self.x_axis, theta]


        if not len(prediction_varriables) == 2:
            raise ValueError("theta is the wrong length")

        return one_neped(*prediction_varriables)

class fit_tanh_class:

    def __init__(self, simulation_profile, x_axis, bounds=None, offset=None):

        self.simulation_profile=simulation_profile
        self.x_axis=x_axis
        self.bounds=bounds
        self.offset=offset

    def cost(self, theta):
        prediction = self.prediction(theta)

        return np.square(self.simulation_profile - prediction).sum()

    def chi_squared(self, theta, normalise=True):
        """
        You want to minimise chi squared to optomise the fit
        
        :param theta: 
        :return: 
        """
        prediction = self.prediction(theta)
        normalised_residuals=(self.simulation_profile - prediction) / self.simulation_profile
        if not normalise:
            return np.square(normalised_residuals)
        chi_squared=np.square(normalised_residuals).sum()
        normalised_chi_squared=chi_squared/len(self.simulation_profile)

        return normalised_chi_squared 

    def prediction(self, theta):
        prediction_varriables=[self.x_axis, *theta]
        if self.offset is not None:
            prediction_varriables.append(self.offset)

        if not len(prediction_varriables)==6:
            raise ValueError("theta is the wrong length")

        return mtanh(*prediction_varriables)

def mtanh(x, position, width, height, slope, offset):


    # option to use -neped or 0
    if offset != 0:
        # -neped must be used
        offset = -height
    """ User defined mtanh function [R. Scannell RSI 2011]"""
    inside = (position - x)/(2.*width)
    mtanh = ((1. + slope*inside)*exp(inside) - exp(-inside))\
        /(exp(inside) + exp(-inside))
    edge = (height - offset)/2.*(mtanh + 1.) + offset

    return edge


def plot_1_neped_line(neped,deltane,axis,line_color_string,neped_start=None,index_neped_user=None):

    min_neped = min(neped)
    max_neped = max(neped)
    if index_neped_user != None:
        # Allows user to select which point to draw line through
        index_min_neped = index_neped_user
        min_deltane = deltane[index_min_neped]
        min_neped = neped[index_min_neped]
    else:
        index_min_neped = np.argmin(neped)
        min_deltane = deltane[index_min_neped]

    prop_const = min_neped * min_deltane
    if neped_start == None:
        x_new = np.linspace(min_neped, max_neped, 100)
    else:
        x_new = np.linspace(neped_start, max_neped, 100)
    axis.plot(x_new, prop_const / x_new, line_color_string)
    return  index_min_neped
def calc_brute(posterior, threads=16,ns=40,use_chi_square=False):

    if use_chi_square == False:
        brute_fit, fit_cost, grid, grid_cost = brute(posterior.cost, ranges=posterior.bounds, Ns=ns,
                                                 workers=threads, full_output=True, finish=None)
    else:
        brute_fit, fit_cost, grid, grid_cost = brute(posterior.chi_squared, ranges=posterior.bounds, Ns=ns,
                                                     workers=threads, full_output=True, finish=None)

    brute_data = posterior.prediction(brute_fit)
    return brute_fit, fit_cost, grid, grid_cost,brute_data
def calc_bfgs(posterior, brute_fit):
    """
            USE THIS IF THE PROBLEM CAN'T FITTED IT CAN HELP
            BE SURE TO PASS IT REASONABLE BOUNDS THOUGH
            """
    # Run minimiser function using brute fit guess
    # Note approx_grad = True needs to be set in order approximate the gradient of the function
    # to be minised else you need to pass it in
    bfgs_fit, bfgs_fit_cost, bfgs_out = fmin_l_bfgs_b(posterior.cost, x0=brute_fit, bounds=posterior.bounds,
                                                     approx_grad=True)
    #
    bfgs_data = posterior.prediction(bfgs_fit)

    return bfgs_fit, bfgs_fit_cost, bfgs_out,bfgs_data
    """ END EXTRA MINIMISER"""

def calc_curve_fit(posterior,fitted_params,curve_bounds):
    f_curve_fit = lambda x, a, b, c, d: mtanh(x, a, b, c, d,
                                              posterior.offset)  # lambda funtion because curve_fit is stupid
    # set up curve fit to be with correct bounds
    if curve_bounds:
        curve_fit_p0, curve_fit_pcov = curve_fit(f_curve_fit, posterior.x_axis, posterior.simulation_profile,
                                             p0=fitted_params
                                             ,bounds=posterior.bounds_curve_fit)
    else:
    #     bounds don't always play nicely with teh curve fit
        print('Curve fit with bounds')
        curve_fit_p0, curve_fit_pcov = curve_fit(f_curve_fit, posterior.x_axis, posterior.simulation_profile,
                                                 p0=fitted_params)

    curve_fit_fit = posterior.prediction(curve_fit_p0)
    return curve_fit_p0, curve_fit_pcov, curve_fit_fit



def one_neped(x,prop_const):

    deltane = prop_const/x
    return deltane
def fit_1_neped_chi_square(neped,deltane):
    posterior = fit_1_neped_class(deltane,neped)
    # bounds for proportionality constant
    posterior.bounds = [(neped[0]*deltane[0],neped[-1]*deltane[-1])]
    fitted_params, fit_cost, grid, grid_cost,fit_data = calc_brute(posterior,ns=80,use_chi_square=True)
    chi_squared = posterior.chi_squared(fitted_params)
    new_x = np.linspace(neped[0],neped[len(neped)-1],100)
    # update the object to have finer x axis

    fitted_line = one_neped(new_x,fitted_params)
    return new_x,fitted_line,chi_squared
def make_mtanh_guess(profile,r_coord,idx_top_barrier,core_depth_index):


    # Set inital gues for neped
    pedestal_top_guess = profile[idx_top_barrier]

    jst_width = ((r_coord[-1]) - (r_coord[idx_top_barrier])) / 4

    ne_arr = profile
    ne_arr = ne_arr  # /ne_arr[0]  # normalise
    # normalise 0 to separatrix for r coordintea
    r_coord = r_coord - r_coord[-1]
    # think minus 1 because of what mtanh sets core slope tobe
    linear_guess = (ne_arr[idx_top_barrier - 1] - (ne_arr[idx_top_barrier - core_depth_index])) / \
                   (r_coord[idx_top_barrier - 1] - r_coord[idx_top_barrier - core_depth_index])

    # slope guess is define weirdly
    slope_guess = (4 * jst_width * -1 * linear_guess) / pedestal_top_guess

    return pedestal_top_guess,jst_width,slope_guess

def  fit_tanh(profile,r_coord,idx_top_of_barrier,core_depth_index,opts,profile_switch):

    # ONLY FOR ONE TIME SLICE!!!!

    """
    REQUIRMENT - PLOT_JST_PEDESTAL.PY IS CALLED BEFORE THIS ROUTINE

    :param simulation_list: list of objects for the simulation class
    :param figure_list: list of figures to be returned
    :param opts: command line options
    :param profile_switch: options 'NE' - density profile fit, 'TE' - electron temperature fit
    :return: TBD
    """


    # Save pedestal parameters to plot them
    neped = []
    deltane = []
    position = []
    chi_square = []
    neped_pos_offset = []
    # fitting options wahat fits to use
    # we ALWAYS use brute as the inital guess
    bfgs_to_fit = opts.bfgs_flag
    curve_fit_to_fit = opts.curve_fit_flag
    curve_fit_bounds = opts.curve_fit_bounds_flag

    # loop over simulations

    # sim.neped_height_offset = []
    # sim.neped_pos_offset = []
    # sim.neped_width_offset = []
    # te_ln = len(simulation.TE_end_time)

    core_cut_off_idx = idx_top_of_barrier - core_depth_index
    profile_data = profile[core_cut_off_idx:]

    # idx_top_barrier=85
    if profile_switch == 'TE':
        # can be different for TE and NE
        fitting_opts_name = "TE_profile"
        # generate guess for fits
        pedestal_top_guess, jst_width, slope_guess = \
            make_mtanh_guess(profile, r_coord, idx_top_of_barrier, core_depth_index)

        print('JST width guess', jst_width)
        print('slope guess', slope_guess)

    elif profile_switch == 'NE':

        fitting_opts_name = "NE_fit"

        # generate guess for fits
        pedestal_top_guess,jst_width,slope_guess = \
            make_mtanh_guess(profile, r_coord, idx_top_of_barrier, core_depth_index)

        print('JST width guess', jst_width)
        print('slope guess', slope_guess)
    else:
        import sys
        sys.exit('Correct issue with calling of tanh fitting')


    """
    SET THE X-AXIS USED 
    """
    r_end_time =r_coord[core_cut_off_idx:]
    position_guess = r_coord[idx_top_of_barrier]
    ########################
    # CONFIGURE BOUNDS AND INITAL GUESS

    # 3.819
    fitting_opts =\
        options_fot_fitting_mtanh.fitting_options(position_guess,pedestal_top_guess,
                                                  jst_width,slope_guess,fitting_opts_name)
    # inital guesses for the fit
    # position = fitting_opts["inital_guess"]["position"]
    # width = fitting_opts["inital_guess"]["width"]
    # height = fitting_opts["inital_guess"]["height"]
    # slope  = fitting_opts["inital_guess"]["slope"]

    # set up bounds

    position_min,position_max = fitting_opts["bounds"]["position_min"], fitting_opts["bounds"]["position_max"]
    width_min, width_max = fitting_opts["bounds"]["width_min"], fitting_opts["bounds"]["width_max"]
    height_min, height_max = fitting_opts["bounds"]["height_min"], fitting_opts["bounds"]["height_max"]
    slope_min, slope_max = fitting_opts["bounds"]["slope_min"], fitting_opts["bounds"]["slope_max"]



    # SET OFFSET
    # becareful if using more than two for plotting the average
    if opts.user_offset == 'neped':
        offset_list = [-pedestal_top_guess]
    elif opts.user_offset == '0':
        offset_list = [0]
    elif opts.user_offset == None:
        offset_list = [0]




    # initilase object
    posterior = fit_tanh_class(profile_data, r_end_time)
    for offset in offset_list:
        print('Fitting profile - ', profile_switch)
        posterior.offset = offset
        posterior.bounds = [(position_min,position_max),(width_min,width_max),(height_min,height_max),(slope_min,slope_max)]
        # curve fit takes silly ordering of bounds
        posterior.bounds_curve_fit = ((position_min,width_min,height_min,slope_min),(position_max,width_max,height_max,slope_max))

        fitted_params, fit_cost, grid, grid_cost,fit_data = calc_brute(posterior)

        if bfgs_to_fit:
            print('bfgs running')
            fitted_params, bfgs_fit_cost, bfgs_out, fit_data = calc_bfgs(posterior,fitted_params)


        if curve_fit_to_fit:
            print('Curve fit running')
            fitted_params, curve_fit_pcov, fit_data = calc_curve_fit(posterior,fitted_params,curve_fit_bounds)

        #     Save data as a list
        # add infortmation to simulation of the fitting
        neped.append(fitted_params[2])
        neped_pos_offset.append(fitted_params[0])
        deltane.append(fitted_params[1] * 4)  # NOTE THE TIMES BY 4 THIS IS BECUASE OF TEH DEFINTION WHICH IS USED FOR THE WIDTH
        print('offset = ', offset)
        print(fitted_params)
        print('Chi sqaured = ', posterior.chi_squared(fitted_params))
        chi_square.append((posterior.chi_squared(fitted_params)))



    #########################################
    # END fitting AND LOOP
    ##########################################


    return neped, deltane, neped_pos_offset, chi_square, fit_data, r_end_time, profile_data
