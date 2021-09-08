# Package imports
import bohek_tabs.plotting_routines.stability_plots as bohek_stability_plots

# Std imports
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def calc_gradients(jsp, slice_idx):

    pre_grad = np.diff(jsp["PRE"].values) / np.diff(jsp["R"].values)
    te_grad = np.diff(jsp["TE"].values) / np.diff(jsp["R"].values)
    ne_grad = np.diff(jsp["NE"].values) / np.diff(jsp["R"].values)
    ti_grad = np.diff(jsp["TI"].values) / np.diff(jsp["R"].values)
    r = (jsp["R"])[0:-1]

    return r[slice_idx:], te_grad[slice_idx:], ne_grad[slice_idx:], ti_grad[slice_idx:], pre_grad[slice_idx:]


def main(simulations):

    # Plots for gradient v. bootstrap
    fig,ax=plt.subplots(nrows=1,ncols=3)
    # Gradient positions v. bootstrap
    fig_pos,ax_pos=plt.subplots(nrows=1,ncols=4,sharey=True)
    # Position of max alpha (electron pre) v. max current (J) in pedestal. Should be aligned
    fig_alpha_j,ax_alpha_j=plt.subplots(nrows=1,ncols=1)

    for simulation in simulations:
        jsp = simulation['JSP_mishka']
        jst = simulation['JST_mishka']
        # PLOT MAX GRAD versus MAX BOOTSTRAP
        max_bootstrap = []
        max_ne_grad = []
        max_pe_grad = []
        max_te_grad =[]
        max_ti_grad =[]

        pos_max_ne_grad = []
        pos_max_te_grad = []
        pos_max_ti_grad = []
        pos_max_jzbs = []
        pos_max_pre_grad = []

        time = []
        time_index = []

        for index in range(0,len(jsp["time"])):
            # Accumlate data
            jsp_single=jsp.isel(time=index)
            # jst_single = jst["time"][index]
            jzbs=jsp_single["JZBS"]


            # So the reason all this is done is to make sure we get the bootstrap peak in the edge
            # sometimes the bootstrap curent has a large contribution in the core I don't know why
            # I shoud investigate this
            # just choose the peak
            slice_idx = int(len(jzbs)*0.7)
            max_bootstrap.append(max(jzbs[slice_idx:]))
            jzbs_slice=((jzbs[slice_idx:]))
            idx_max_bootstrap = np.argmax(jzbs_slice.values) #this is still xarray check what is needed
            r,te_grad,ne_grad,ti_grad,pre_grad = calc_gradients(jsp_single,slice_idx)
            te_slice = (jsp_single["TE"][slice_idx:]).values
            ne_slice = (jsp_single["NE"][slice_idx:]).values
            ti_slice = (jsp_single["TI"][slice_idx:]).values

            # calc prefactors in bootstrap current
            ne_multi = 2.44*(te_slice[idx_max_bootstrap]+ti_slice[idx_max_bootstrap])
            te_multi=0.69*ne_slice[idx_max_bootstrap]
            ti_multi=0.42*ne_slice[idx_max_bootstrap]

            # Take the position of maximum bootstrap current
            # if te_grad.any() or ne_grad.any() or ti_grad.any() or pre_grad.any() > 0:
            #     print("POSTIVE GRADIENT FOUND")
            max_ne_grad.append(ne_grad[idx_max_bootstrap]*ne_multi)
            max_pe_grad.append(pre_grad[idx_max_bootstrap])
            max_te_grad.append(te_grad[idx_max_bootstrap]*te_multi)
            max_ti_grad.append(ti_grad[idx_max_bootstrap]*ti_multi)
            time.append(jsp_single["time"])
            time_index.append(index)

            min_te_idx = np.argmin(te_grad)
            min_ti_idx = np.argmin(ti_grad)
            min_ne_idx = np.argmin(ne_grad)
            min_pre_idx = np.argmin(pre_grad)
            max_jzbs_idx = np.argmax(jzbs_slice.values)
            pos_max_ne_grad.append(r[min_ne_idx])
            pos_max_te_grad.append(r[min_te_idx])
            pos_max_ti_grad.append(r[min_ti_idx])
            pos_max_jzbs.append(r[max_jzbs_idx])
            pos_max_pre_grad.append(r[min_pre_idx])

        im = ax[0].scatter(max_bootstrap,max_ne_grad,marker=simulation.marker,
                label=simulation.label,c=time_index)

        im1 = ax[1].scatter(max_bootstrap, max_te_grad, marker=simulation.marker,
                      label=simulation.label,c=time_index)

        im2 = ax[2].scatter(max_bootstrap,max_ti_grad, marker=simulation.marker,
                      label=simulation.label,c=time_index)

        im_pos = ax_pos[0].scatter(max_bootstrap, pos_max_ne_grad, marker=simulation.marker,
                           label=simulation.label, c=time_index)

        im1_pos = ax_pos[1].scatter(max_bootstrap, pos_max_te_grad, marker=simulation.marker,
                            label=simulation.label, c=time_index)

        im2_pos = ax_pos[2].scatter(max_bootstrap, pos_max_ti_grad, marker=simulation.marker,
                            label=simulation.label, c=time_index)

        im3_pos = ax_pos[3].scatter(max_bootstrap, pos_max_jzbs, marker=simulation.marker,
                                    label=simulation.label, c=time_index)

        im1_alpha_j = ax_alpha_j.scatter(pos_max_pre_grad, pos_max_jzbs, marker=simulation.marker,
                                    label=simulation.label, c=time_index)


    # ax[0].set_ylim(bottom=0)
    ax[0].ticklabel_format(axis='y', style='sci', scilimits=(0, 0))
    ax[0].ticklabel_format(axis='x', style='sci', scilimits=(0, 0))
    ax[0].set_xlabel("Bootstrap")
    ax[0].set_ylabel("ne grad(T_e+T_i) @ max J in etb coef = "+str(ne_multi))
    # fig.colorbar(im,ax=ax[0])
    ax[2].legend()

    # ax[1].set_ylim(bottom=0)
    ax[1].ticklabel_format(axis='y', style='sci', scilimits=(0, 0))
    ax[1].ticklabel_format(axis='x', style='sci', scilimits=(0, 0))
    ax[1].set_xlabel("Bootstrap")
    ax[1].set_ylabel("te grad * n @ max J in etb coef ="+str(te_multi))
    # fig.colorbar(im1,ax=ax[1])

    ax[2].set_xlabel("Bootstrap")
    ax[2].set_ylabel("ti grad * n @ max J in etb coef = "+str(ti_multi))
    # ax[2].set_ylim(bottom=0)
    ax[2].ticklabel_format(axis='y', style='sci', scilimits=(0, 0))
    ax[2].ticklabel_format(axis='x', style='sci', scilimits=(0, 0))
    fig.colorbar(im2,ax=ax[2])

    ax_pos[0].ticklabel_format(axis='y', style='sci', scilimits=(0, 0))
    ax_pos[0].ticklabel_format(axis='x', style='sci', scilimits=(0, 0))
    ax_pos[0].set_xlabel("max Bootstrap")
    ax_pos[0].set_ylabel("max ne grad position")
    # fig.colorbar(im,ax=ax[0])
    ax_pos[2].legend()

    # ax[1].set_ylim(bottom=0)
    ax_pos[1].ticklabel_format(axis='y', style='sci', scilimits=(0, 0))
    ax_pos[1].ticklabel_format(axis='x', style='sci', scilimits=(0, 0))
    ax_pos[1].set_xlabel("max Bootstrap")
    ax_pos[1].set_ylabel("max te grad position")
    # fig.colorbar(im1,ax=ax[1])

    ax_pos[2].set_xlabel("max Bootstrap")
    ax_pos[2].set_ylabel("max ti grad position")
    # ax[2].set_ylim(bottom=0)
    ax_pos[2].ticklabel_format(axis='y', style='sci', scilimits=(0, 0))
    ax_pos[2].ticklabel_format(axis='x', style='sci', scilimits=(0, 0))
    # fig_pos.colorbar(im2_pos, ax=ax_pos[2])

    ax_pos[3].set_xlabel("max Bootstrap")
    ax_pos[3].set_ylabel("Position of Max bootstrap edge")
    # ax[2].set_ylim(bottom=0)
    ax_pos[3].ticklabel_format(axis='y', style='sci', scilimits=(0, 0))
    ax_pos[3].ticklabel_format(axis='x', style='sci', scilimits=(0, 0))
    fig_pos.colorbar(im3_pos, ax=ax_pos[3])


    # ANOTHER FIGURE
    ax_alpha_j.set_ylabel('Position of max current in pedestal')
    ax_alpha_j.set_xlabel('Position of max electron pressure gradient in pedestal')
    fig_alpha_j.colorbar(im1_alpha_j, ax=ax_alpha_j)
    fig_alpha_j.legend()


