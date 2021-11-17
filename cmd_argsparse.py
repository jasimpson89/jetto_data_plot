import argparse
def parse_opt(parents=[]):
    parser = argparse.ArgumentParser(parents=parents, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    # labels for plots

    parser.add_argument("-x", dest="x",
                        action="store", default='R', type=str,
                        help="Choice of x axis for the plots")


    parser.add_argument("-bfgs", dest="bfgs_flag",
                        action="store_true",default=False,
                        help="Use bfgs to fit the profile along with brute and other options selected")

    parser.add_argument("-bohek", dest="use_bohek_tabs",
                        action="store_true", default=False ,
                        help="Turn on and off Bohek tabs, if not set to true matplotlib will be used")

    parser.add_argument("-curve_fit", dest="curve_fit_flag",
                        action="store_true", default=False,
                        help="Use curvefit to fit the profile along with brute and other options selected")

    parser.add_argument("-curve_fit_bounds", dest="curve_fit_bounds_flag",
                        action="store_false",
                        help="Use bounds on curve fit that were the same as brute and bfgs (if used) "
                             "can be used to resolve /n odd things curve does some times")

    parser.add_argument("-offset", dest="user_offset",
                        action="store",default=None,choices=["neped","0"],
                        help="Set offset to be used for mtanh fitting")

    parser.add_argument("-mtanh", dest="mtanh",
                        action="store_true", default=False,
                        help="Doe mtanh fitting which can be slow")

    parser.add_argument("-plotly", dest="plotly",
                        action="store_true", default=False,
                        help="Runs the plotly interface")
    

    parser.add_argument("-ppf", dest="ppf",
                        action="store_true", default=False,
                        help="Gets the fits from Lorenzo database for plotting")

    
    parser.add_argument("-hrts", dest="hrts",
                        action="store_true", default=False,
                        help="Gets HRTS data for fitting")

    parser.add_argument("-l", "--labels", dest="labels",
                            action="store", default=None, nargs='+', type=str,
                            help="Labels for runs")    

    parser.add_argument("-s", "--simulations", dest="jetto_runs",
                           action="store", nargs='+', type=str, default=None,
                           help="Simulations to be plotted, assuming they are stored in "                                                                 
                                "/commons/cmg/$USER/jetto/runs")



    # End statement to parse the inputs
    
    opts = parser.parse_args()

    return opts
