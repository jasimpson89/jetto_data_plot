import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.animation import FuncAnimation
matplotlib.use('Qt5Agg')
def plot_stab_boundary(alpha,current,simulation_list):
    """

    :param alpha: 2D array [simulation][data]
    :param current: [simulation][data]
    :return:
    """
    fig_single, ax_single = plt.subplots(nrows=1, ncols=1)
    # time
    for i in range(len(alpha[0][:])):
        # simulation
        a = []
        jb = []
        for j in range(len(alpha)):
            a.append((alpha[j][i]))
            jb.append(current[j][i])
            # "operation point"
            ax_single.plot(alpha[j][i], current[j][i], color=simulation_list[j].color,marker=simulation_list[j].marker,ms=15)

        # line boundary
        ax_single.plot(a,jb,linestyle='-',label='time - '+str(i))
    ax_single.legend()

def make_j_alpha_scatter_animation():
    fig, ax = plt.subplots(figsize=(5, 3))
    ax.set(xlim=(-3, 3), ylim=(-1, 1))

def make_j_alpha_scatter(subplot,rows,cols,simulation,time,alpha,bootstrap,unstable_mode,
                         alfm_plot_pre_elm,cubs_plot_pre_elm):

    if cols == 1 and rows ==1:
        # subplot.plot(alfm_plot_pre_elm, cubs_plot_pre_elm, marker=simulation.marker
        #                        , ms=10, color=simulation.color, alpha=0.2)

        # Add unstable mode
        marker_string = u'$' + str(unstable_mode) + '$'  # need a unicode string and MATH mode for the marker
        subplot.plot(alpha, bootstrap, label=simulation.label, marker=marker_string
                               , ms=20, color=simulation.color)
        # Scientific Axis
        subplot.ticklabel_format(axis='y', style='sci', scilimits=(0, 0))

        return subplot



    j = 0
    for col in range(0,cols):
        for row in range(0,rows):
            subplot[col,row].set_title(time[j])

            # Plot pre elm values
            subplot[col,row].plot(alfm_plot_pre_elm[j],cubs_plot_pre_elm[j],marker=simulation.marker
                                  ,ms=10,color=simulation.color,alpha=0.2)

            # Add unstable mode
            marker_string = u'$'+str(unstable_mode[j])+'$' # need a unicode string and MATH mode for the marker
            subplot[col, row].plot(alpha[j], bootstrap[j], label=simulation.label, marker=marker_string
                                   , ms=15, color=simulation.color)
            # Scientific Axis
            subplot[col, row].ticklabel_format(axis='y', style='sci',scilimits=(0,0))
            j+=1



    return subplot

def find_pre_elm_profiles(simulation):
    time = (simulation["JST"])["time"]
    unstable_time = (simulation["JST_mishka"])["time"]
    idx = [] # index for pre elm profile
    for t in unstable_time:
        # NOTE np.where didn't seem to work
        idx_t = (np.abs(time - t)).argmin() # this should almost be an exact match

        idx.append(idx_t-1)

    def select_pre_data(jst,idx,phys_id):
        var = jst[phys_id]
        return var[idx]

    pre_elm_alpha = select_pre_data(simulation["JST"],idx,"ALFM")
    pre_elm_bootstrap = select_pre_data(simulation["JST"],idx,"CUBS")

    return pre_elm_alpha, pre_elm_bootstrap

def main(simulation_data):
    # NOTE COLS AND ROWS SHOULD BE SAME NUMBER

    no_cols = 2
    no_rows = 2
    tot_plots = no_cols * no_rows
    fig, ax = plt.subplots(no_rows, no_cols, sharex=True, sharey=True)

    alfm_animation=[]
    cubs_animation = []
    for simulation in simulation_data:

        if simulation.load_jst == True:
            mishka_data_with_jst = simulation['JST_mishka']
            if simulation['no_unstable_modes'] == True:
                # break out the routine
                return

            if tot_plots ==1:
                time_plot = ((mishka_data_with_jst["time"])[-1]).values
                alfm_plot = ((mishka_data_with_jst["ALFM"])[-1]).values
                cubs_plot = ((mishka_data_with_jst["CUBS"])[-1]).values
                unstable_mode_plot = ((mishka_data_with_jst["unstable_mode"])[-1]).values
            else:
                time_plot = ((mishka_data_with_jst["time"])[-tot_plots:]).values
                alfm_plot = ((mishka_data_with_jst["ALFM"])[-tot_plots:]).values
                cubs_plot = ((mishka_data_with_jst["CUBS"])[-tot_plots:]).values
                unstable_mode_plot = ((mishka_data_with_jst["unstable_mode"])[-tot_plots:]).values



            alfm_plot_pre_elm, cubs_plot_pre_elm = find_pre_elm_profiles(simulation)
            ax = make_j_alpha_scatter(ax, no_rows, no_cols, simulation, time_plot,
                                      alfm_plot, cubs_plot,unstable_mode_plot,
                                      alfm_plot_pre_elm,cubs_plot_pre_elm)

            alfm_animation.append(alfm_plot)
            cubs_animation.append(cubs_plot)




    # THIS MAKES LARGE AXIS SO WE CAN MAKE A COMMON X & Y LABELS
    fig.add_subplot(111, frameon=False)
    # hide tick and tick label of the big axis
    plt.tick_params(labelcolor='none', top=False, bottom=False, left=False, right=False)
    plt.xlabel("Max Alpha in ETB")
    plt.ylabel("Max boostrap")
    if no_rows > 1 and no_cols > 1:
        ax[0,0].legend()
    else:
        ax.legend()

    plot_stab_boundary(alfm_animation,cubs_animation,simulation_data)

