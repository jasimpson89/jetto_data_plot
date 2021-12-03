# Pkg imports
import analysis_routines.mtanh_fitting.mtanh_interface as mtanh_interface
import analysis_routines.pedestal_database_reader.read_plot_samuli_data as read_exp_ped_data

# Std imports
import matplotlib.pyplot as plt

def plot_exp_ped_height_width(df):
    fig_nesep_peped, ax_nesep_peped = plt.subplots(nrows=2, ncols=4)

    # teped
    ax_nesep_peped[0,0].scatter(df.nesep, df.teped)
    ax_nesep_peped[0,0].set_xlabel(r'$n_{e,sep} (10^{19})$')
    ax_nesep_peped[0,0].set_ylabel(r'$T_{e,ped}$ keV')

    # neped
    ax_nesep_peped[0,1].scatter(df.nesep, df.neped)
    ax_nesep_peped[0,1].set_xlabel(r'$n_{e,sep} (10^{19})$')
    ax_nesep_peped[0,1].set_ylabel(r'$n_{e,ped} (10^{19})$')

    # te width
    ax_nesep_peped[1,0].scatter(df.nesep, df.deltate_cm/100)
    ax_nesep_peped[1,0].set_xlabel(r'$n_{e,sep} (10^{19})$')
    ax_nesep_peped[1,0].set_ylabel(r'$\Delta_{te} (m)$')

    # ne width
    ax_nesep_peped[1,1].scatter(df.nesep, df.deltane_cm/100)
    ax_nesep_peped[1,1].set_xlabel(r'$n_{e,sep} (10^{19})$')
    ax_nesep_peped[1,1].set_ylabel(r'$\Delta_{ne} (m)$')

    # pe height
    ax_nesep_peped[0,2].scatter(df.nesep, df.peped)
    ax_nesep_peped[0,2].set_xlabel(r'$n_{e,sep} (10^{19})$')
    ax_nesep_peped[0,2].set_ylabel(r'$p_{e,ped} (kPa)$')


    # Total particle content
    ax_nesep_peped[1,2].scatter(df.nesep, df.neped*df.plasma_volume)
    ax_nesep_peped[1,2].set_xlabel(r'$n_{e,sep} (10^{19})$')
    ax_nesep_peped[1,2].set_ylabel('Approx particle content \n'r'$n_{e,ped} * Vol_{plasma} (10^{19}$)')

    # Pressure pedestal width
    ax_nesep_peped[0,3].scatter(df.nesep, df.deltape_cm/100)
    ax_nesep_peped[0,3].set_xlabel(r'$n_{e,sep} (10^{19})$')
    ax_nesep_peped[0,3].set_ylabel(r'$\Delta_{pe}$ from mtanh')

    return ax_nesep_peped

def main(simulation_list,opts):

    # Get experimental data
    
    pe_nesep_exp_df,stability_df,pe_nesep_exp_stability_filter_df = read_exp_ped_data.main()
    # ax_nesep_peped.scatter(pe_nesep_exp_df.nesep,pe_nesep_exp_df.peped)
    
    
    fig_nesep_peped,ax_nesep_peped = plt.subplots(nrows=1,ncols=1)
    ax_nesep_peped.set_xlim(xmin=0)
    ax_nesep_peped.set_ylim(ymin=0)
    ax_nesep_peped.set_xlabel(r'$n_{e,sep} / n_{e,ped}$')
    ax_nesep_peped.set_ylabel(r'$P_{e,ped}$ kPA')



    ax_nesep_pedestal_parm = plot_exp_ped_height_width(pe_nesep_exp_df)

    fig_alpha_j,[[ax_alpha,ax_j],[ax_ratio_alpha,ax_ratio_j]] = plt.subplots(nrows=2,ncols=2)



    alpha_crit = pe_nesep_exp_stability_filter_df['crit.alpha raw']
    alpha_crit_exp = pe_nesep_exp_stability_filter_df['exp.alpha']

    j_crit = pe_nesep_exp_stability_filter_df['exp.<j>']
    j_crit_exp = pe_nesep_exp_stability_filter_df['crit<j> raw']

    j_crit_ratio = j_crit / j_crit_exp
    alpha_crit_ratio = alpha_crit / alpha_crit_exp

    ax_alpha.scatter(pe_nesep_exp_stability_filter_df.nesep, pe_nesep_exp_stability_filter_df['crit.alpha raw'],marker='o')
    ax_alpha.scatter(pe_nesep_exp_stability_filter_df.nesep, pe_nesep_exp_stability_filter_df['exp.alpha'],marker='d')

    ax_j.scatter(pe_nesep_exp_stability_filter_df.nesep, pe_nesep_exp_stability_filter_df['crit<j> raw']*1e6,marker='o')
    ax_j.scatter(pe_nesep_exp_stability_filter_df.nesep, pe_nesep_exp_stability_filter_df['exp.<j>']*1e6,marker='d')

    ax_ratio_alpha.scatter(pe_nesep_exp_stability_filter_df.nesep, alpha_crit_ratio,c=pe_nesep_exp_stability_filter_df['crit. n diam'],marker='o')
    im = ax_ratio_j.scatter(pe_nesep_exp_stability_filter_df.nesep, j_crit_ratio,c=pe_nesep_exp_stability_filter_df['crit. n diam'],marker='o')
    fig_alpha_j.colorbar(im, ax=ax_ratio_j)

    ax_nesep_peped.set_xlim(xmin=0)
    ax_nesep_peped.set_ylim(ymin=0)
    ax_alpha.set_xlabel(r'$n_{e,sep}$')

    ax_alpha.set_ylabel(r'$\alpha_{max,ped}$')
    ax_j.set_xlabel(r'$n_{e,sep}$')
    ax_j.set_ylabel(r'$J_{max,ped}$')

    ax_ratio_alpha.set_xlabel(r'$n_{e,sep}$')
    ax_ratio_alpha.set_ylabel(r'$\alpha_{crit}/ \alpha_{exp}$')
    ax_ratio_j.set_xlabel(r'$n_{e,sep}$')
    ax_ratio_j.set_ylabel(r'$j_{crit}/ j_{exp}$')


    # Plot the fits
    fig_fit,[ax_te_fit, ax_ne_fit] = plt.subplots(nrows=1,ncols=2)
    ax_te_fit.set_ylabel('TE')
    ax_ne_fit.set_ylabel('NE')

    ax_nesep_peped.scatter(pe_nesep_exp_df.nesep/pe_nesep_exp_df.neped,pe_nesep_exp_df.peped)
    ax_nesep_peped.set_xlim(xmin=0)
    ax_nesep_peped.set_ylim(ymin=0)
    ax_nesep_peped.set_xlabel(r'$n_{e,sep}/n_{e,ped}$')
    ax_nesep_peped.set_ylabel(r'$P_{e,ped}$ kPA')

    for simulation in simulation_list:

        # Make mtanh fits
        # pythonistas say i shoudl use try except here rather than hasatttr its slower
        if hasattr(simulation, "mtanh_fit_time"):
            # time can be specified in the JSON file
            time = simulation.mtanh_fit_time
            jst = simulation["JST"].sel(time=time,method='nearest')
            # compare to experiment
            jsp = simulation['JSP'].sel(time=time, method='nearest')

        elif simulation["JST_mishka"]:
            ## select last unstable time
            jst = simulation["JST_mishka"].isel(time=-1)
            time = float(jst.coords["time"])
            # compare to experiment
            jsp = simulation['JSP'].sel(time=time, method='nearest')

        nesep = ((jsp['NE'])[-1]).values

        if opts.mtanh == True:
            teped, deltate, te_offset, chi_square_te, te_fit_data, te_r_end_time,te_orig_data =\
                mtanh_interface.fit_one_profile(simulation,opts,'TE',time)
            neped, deltane, ne_offset, chi_square_ne, ne_fit_data, ne_r_end_time,ne_orig_data =\
                mtanh_interface.fit_one_profile(simulation,opts,'NE',time)
            # its an array due to the offsets that can be used in the mtanh fit
            preped = (neped[0]*teped[0]*1.6E-19)/1e3 # kPa
            #
            nesep = ((jsp['NE'])[-1]).values
            ax_nesep_peped.plot(nesep / 1e19, preped, marker=simulation.marker, color=simulation.color,
                                label=simulation.label,ms=15)
            top_barrier_idx = int(jst['JTOB'])

            ax_nesep_peped.plot(nesep / 1e19, float(jsp['PRE'][top_barrier_idx])/1e3, marker=simulation.marker,
                                color=simulation.color,
                                label=simulation.label, alpha=0.4,ms=15)

            # FROM FIT
            ax_nesep_pedestal_parm[0,0].plot(nesep/1e19,teped[0]/1e3,marker=simulation.marker,color=simulation.color,
                                             label=simulation.label,ms=15, alpha=0.5)
            ax_nesep_pedestal_parm[0,1].plot(nesep/1e19,neped[0]/1e19,marker=simulation.marker,color=simulation.color,
                                             label=simulation.label,ms=15, alpha=0.5)
            ax_nesep_pedestal_parm[1, 0].plot(nesep/1e19, deltate, marker=simulation.marker, color=simulation.color,
                                      label=simulation.label,ms=15, alpha=0.5)
            ax_nesep_pedestal_parm[1, 1].plot(nesep/1e19, deltane, marker=simulation.marker, color=simulation.color,
                                      label=simulation.label,ms=15, alpha=0.5)


            # Plot fits
            ax_ne_fit.plot(ne_r_end_time,ne_orig_data,linestyle='-',color=simulation.color,label=simulation.label)
            ax_ne_fit.plot(ne_r_end_time,ne_fit_data,linestyle='--',color=simulation.color,label=simulation.label+' fit')

            ax_te_fit.plot(te_r_end_time, te_orig_data, linestyle='-', color=simulation.color, label=simulation.label)
            ax_te_fit.plot(te_r_end_time, te_fit_data, linestyle='--', color=simulation.color,
                           label=simulation.label + ' fit')
            ax_ne_fit.legend()

        #END LOOP


        # FROM JST
        ax_nesep_pedestal_parm[0, 0].plot(nesep / 1e19, jst['TEBA'] / 1e3, marker=simulation.marker,ms=15,
                                          color=simulation.color, label=simulation.label,alpha=1.0)
        ax_nesep_pedestal_parm[0, 1].plot(nesep / 1e19, jst['NEBA'] / 1e19, marker=simulation.marker,ms=15,
                                          color=simulation.color, label=simulation.label,alpha=1.0)
        # NOT SURE IF I CAN DO THIS BECAUSE OF WDITH IS APPLIED TO PRESSURE
        # i can delta(ne)=delta(te)=delta(pe)
        r = jsp['R'].values
        psi = jsp['XPSI'].values
        pedestal_width = r[-1] - r[int(jst['JTOB'])]
        pedestal_width_psi = psi[-1] - psi[int(jst['JTOB'])]
        ax_nesep_pedestal_parm[1, 0].plot(nesep / 1e19, pedestal_width, marker=simulation.marker, color=simulation.color,
                                          label=simulation.label,alpha=1.0,ms=15)
        ax_nesep_pedestal_parm[1, 1].plot(nesep / 1e19, pedestal_width, marker=simulation.marker, color=simulation.color,
                                          label=simulation.label,alpha=1.0,ms=15)

        ax_nesep_pedestal_parm[0, 3].plot(nesep / 1e19, pedestal_width, marker=simulation.marker, color=simulation.color,
                                          label=simulation.label,alpha=1.0,ms=15)


        peped = (jst['TEBA'] * jst['NEBA'] * 1.6E-19)/1e3
        ax_nesep_pedestal_parm[0, 2].plot(nesep / 1e19, peped, marker=simulation.marker, color=simulation.color,
                                          label=simulation.label, alpha=1.0, ms=15)

        compareable_particle_content = (jst['NEBA']/1e19)*jst['VOL'] # normalise for the ped database
        ax_nesep_pedestal_parm[1, 2].plot(nesep / 1e19,compareable_particle_content , marker=simulation.marker, color=simulation.color,
                                          label=simulation.label, alpha=1.0, ms=15)

        ax_nesep_peped.plot((nesep/jst['NEBA']), peped, marker=simulation.marker, color=simulation.color,
                            label=simulation.label, ms=15)


        # Different plot
        ax_alpha.plot(nesep / 1e19, jst['ALFM'], marker=simulation.marker,ms=15,
                                          color=simulation.color, label=simulation.label,alpha=0.4)
        ax_j.plot(nesep / 1e19, jst['CUBS'] , marker=simulation.marker,ms=15,
                                          color=simulation.color, label=simulation.label,alpha=0.4)

        # legend = ax_nesep_pedestal_parm[1,1].legend()
        # legend.draggable(state=True)

        print("Case - ", simulation.label)
        print('Pedestal with = ', pedestal_width_psi)


        legend = ax_nesep_peped.legend()
