import matplotlib.pyplot as plt
def calc_max_alpha(jsp):
    """
        The maximum alphs is not always output if the ETB model is not active so we can calculate it from the JST
        It should yield the same as give by the time trace
        :return: maximum alpha from the JSP signal
    """

    max_alpha= []
    for i in range(0,len(jsp['ALFV'])):
        alpha = max(jsp['ALFV'][i].values)
        max_alpha.append(alpha)

    return max_alpha

def calc_max_boot_strap_current(jsp):
    """
        Output the maximum bootstrap current
        :return: maximum alpha from the JSP signal
    """

    max_bootstrap_current= []
    for i in range(0,len(jsp['ALFV'])):
        current = max(jsp['JZBS'][i].values)
        max_bootstrap_current.append(current)

    return max_bootstrap_current
def plot_jst(simulations):


    fig_ped, ped_profiles_ax = plt.subplots(ncols=3, nrows=2, sharey=False, sharex=False)

    for simulation in simulations:
        jst = simulation['JST']
        jsp = simulation['JSP']


        max_alpha = calc_max_alpha(jsp)
        max_current = calc_max_boot_strap_current(jsp)

        max_alpha = jst['ALFM']
        max_alpha_x = jst['time'].values
        time = jst['time'].values
        time_jsp = jsp['time'].values
        # ped_profiles_ax[0, 0].set_title('Electron density')
        # ped_profiles_ax[0, 1].set_title('Electron temperature')
        # ped_profiles_ax[0, 2].set_title('Bootstrap current max')
        # ped_profiles_ax[1, 0].set_title('Ion Temperature')
        # ped_profiles_ax[1, 1].set_title('Alpha max')
        # ped_profiles_ax[1, 2].set_title('Electron pressure')

        ped_profiles_ax[0, 0].plot(time, jst['NEBA'],color=simulation.color, label=simulation.label)
        ped_profiles_ax[0, 0].set_xlabel('Time (s)')
        ped_profiles_ax[0, 0].set_ylabel(r'$N_{e, ped top}$')

        ped_profiles_ax[0, 1].plot(time, jst['TEBA'],color=simulation.color, label=simulation.label)
        ped_profiles_ax[0, 1].set_xlabel('Time (s)')
        ped_profiles_ax[0, 1].set_ylabel('$T_{e, ped top}$')

        ped_profiles_ax[1, 0].plot(time, jst['TIBA'],color=simulation.color, label=simulation.label)
        ped_profiles_ax[1, 0].set_xlabel('Time (s)')
        ped_profiles_ax[1, 0].set_ylabel('$T_{i, ped top}$')

        ped_profiles_ax[0, 2].plot(time, jst['TEBA']*jst['NEBA'],color=simulation.color, label=simulation.label)
        ped_profiles_ax[0, 2].set_xlabel('Time (s)')
        ped_profiles_ax[0, 2].set_ylabel('$p_{e, ped top}$')

        ped_profiles_ax[1, 1].plot(time, max_alpha,color=simulation.color, label=simulation.label)
        ped_profiles_ax[1, 1].set_xlabel('Time (s)')
        ped_profiles_ax[1, 1].set_ylabel(r'$\alpha_{max}$')


        ped_profiles_ax[1, 2].plot(time_jsp, max_current,color=simulation.color, label=simulation.label)
        ped_profiles_ax[1, 2].set_xlabel('Time (s)')
        ped_profiles_ax[1, 2].set_ylabel(r'$j_{boostrap,max}$')


    fig_ped.subplots_adjust(right=0.75)
    ped_profiles_ax[1,2].legend(bbox_to_anchor=(1.04,0.5),loc='center left',labelspacing=1.2)

    fig_ped.tight_layout()

