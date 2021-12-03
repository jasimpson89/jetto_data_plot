import numpy as np
import matplotlib.pyplot as plt
def setup_plot_axis():
    # use this routine configure the axes you need and the details
    fig_profiles, [[te_ax,ne_ax],[ti_ax,pre_ax]] = plt.subplots(ncols=2,nrows=2)
    
    te_ax.set_xlabel(r'$\psi_n$')
    te_ax.set_ylabel(r'$T_e eV$')
    
    ne_ax.set_xlabel(r'$\psi_n$')
    ne_ax.set_ylabel(r'$n_e m^{-3}$')

    ti_ax.set_xlabel(r'$\psi_n$')
    ti_ax.set_ylabel(r'$t_i eV$')

    pre_ax.set_xlabel(r'$\psi_n$')
    pre_ax.set_ylabel(r'$P_e Pa$')



    return fig_profiles, te_ax, ne_ax, ti_ax, pre_ax

def setup_plot_axis_transport():
    # use this routine configure the axes you need and the details
    fig_profiles, [chi_ax,d_perp_ax,neo_ax] = plt.subplots(ncols=1,nrows=3)
    
    chi_ax.set_xlabel(r'$\psi_n$')
    chi_ax.set_ylabel(r'$\chi eV$')
    
    d_perp_ax.set_xlabel(r'$\psi_n$')
    d_perp_ax.set_ylabel(r'$d_{\perp}$')
    
    neo_ax.set_xlabel(r'$\psi_n$')
    neo_ax.set_ylabel(r'$neocalssical$')
    


    return fig_profiles, chi_ax,d_perp_ax,neo_ax
def plot_jsp(simulations):
    
    # Set up plots for kinetic profiles
    fig_profiles, te_ax, ne_ax, ti_ax, pre_ax = setup_plot_axis()

    # Set up plots for transport profiles
    fig_transport, chi_ax,d_perp_ax,neo_ax = setup_plot_axis_transport()

    for simulation in simulations:
        # Take the unstable time
        jsp = simulation['JSP_mishka'].isel(time=-1)
        jst = simulation['JST_mishka'].isel(time=-1)

        # Plot the position of the pedestal top, this assumes te=ne in the pedestal top positions
        jtob = int(jst['JTOB'])
        ped_pos = jsp['XPSI'][jtob+1]
        te_ax.axvline(ped_pos,linestyle=simulation.linestyle,color=simulation.color)
        ne_ax.axvline(ped_pos,linestyle=simulation.linestyle,color=simulation.color)
        pre_ax.axvline(ped_pos,linestyle=simulation.linestyle,color=simulation.color)
        ti_ax.axvline(ped_pos,linestyle=simulation.linestyle,color=simulation.color)
        chi_ax.axvline(ped_pos,linestyle=simulation.linestyle,color=simulation.color)
        d_perp_ax.axvline(ped_pos,linestyle=simulation.linestyle,color=simulation.color)
        neo_ax.axvline(ped_pos,linestyle=simulation.linestyle,color=simulation.color)

        
        # Plot out kinetic profiles
        te_ax.plot(jsp['XPSI'],jsp['TE'],linestyle=simulation.linestyle,color=simulation.color,linewidth=1,label=simulation.label)
        ne_ax.plot(jsp['XPSI'],jsp['NE'],linestyle=simulation.linestyle,color=simulation.color,linewidth=1,label=simulation.label)
        pre_ax.plot(jsp['XPSI'],jsp['PRE'],linestyle=simulation.linestyle,color=simulation.color,linewidth=1,label=simulation.label)
        ti_ax.plot(jsp['XPSI'],jsp['TI'],linestyle=simulation.linestyle,color=simulation.color,linewidth=1,label=simulation.label)

        # Plot out transport profiles
        
        xdata = jsp['XPSI'][0:len(jsp['XPSI'])-1]
        chi_ax.plot(xdata,jsp['XE'],linestyle=simulation.linestyle,color=simulation.color,linewidth=1,label=simulation.label)
        d_perp_ax.plot(xdata,jsp['D1'],linestyle=simulation.linestyle,color=simulation.color,linewidth=1,label=simulation.label)
        neo_ax.plot(xdata,jsp['DNCI'],linestyle=simulation.linestyle,color=simulation.color,linewidth=1,label=simulation.label)