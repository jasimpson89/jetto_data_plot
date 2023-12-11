import analysis_routines.mtanh_fitting.fit_mtanh_v3_NE_and_TE as fit_mtanh


def fit_one_profile(sim,opts,phys_id,time):

    """

    This routine allows the mtanh fitting routine to be abstracted from the data source. This way there
    are no call to the xarray object which is produced by the jetto class. I wanted to do this to make the
    routine portable

    :param sim: simulation object
    :param opts: command line options
    :param phys_id: either NE or TE for the fit
    :param time: time at which to do the fit
    :return: returns the fit parameters


    """

    jsp = (sim["JSP"]).sel(time=time,method='nearest')
    jst = (sim["JST"]).sel(time=time,method='nearest')
    profile = (jsp[phys_id]).values # basically either NE or TE
    if opts.x == 'r':
        r_coord = (jsp["R"]).values
    elif opts.x == 'psi':
        r_coord = (jsp["XPSI"]).values
    idx_top_of_barrier = int(jst["JTOB"]) # JETTO gives the index of the top of the pedestal
    core_depth_index = 20 # this is the index of how far to go into the core to do the linear fit guess
    profile_switch = phys_id

    neped, deltane, neped_pos_offset, chi_square, fit_data, r_end_time, orig_data = \
        fit_mtanh.fit_tanh(profile,r_coord,idx_top_of_barrier,core_depth_index,opts,profile_switch)

    return neped, deltane, neped_pos_offset, chi_square, fit_data, r_end_time,orig_data


