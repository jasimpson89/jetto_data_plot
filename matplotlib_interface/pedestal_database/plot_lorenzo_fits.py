from jet.data import sal
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt



def shift(te,ne,xaxis,te_at_sep = 100):

    # find the 100 eV point first

    idx_at_tesep = (np.abs(te-te_at_sep).argmin())
    x_at_tesep = xaxis[idx_at_tesep]

    shifted_te_profile = te[0:idx_at_tesep]
    shifted_ne_profile = ne[0:idx_at_tesep]
    shifted_x_axis = np.linspace(0,1,len(xaxis[0:idx_at_tesep]))
    print(len(shifted_te_profile),len(shifted_x_axis))
    return shifted_x_axis, shifted_ne_profile,shifted_te_profile
def calc_deriv(x,y):
    dydx = []

    for i in range(0,len(x)-1):
        dx = x[i+1]-x[i]
        dy = y[i+1]-y[i]
        diff = dy/dx
        dydx.append(diff)
    return dydx

def read_sal(data_var,part_1,seq_no):
    # this routine is quite specific to carines data
    path = part_1+data_var+':'+seq_no
    print(path)
    try:
        data = sal.get(path)
    except:
        print('Error with PPF reading of {ppf}'.format(ppf=path))
        # this is a bad way of handling this
        return np.array(None), np.array(None)

    ydata_1st_time = data.data[0][:]  # choose first time

    xdata_1st_time = data.dimensions[1].data

    # slice y data
    idx = (np.abs(xdata_1st_time- 1)).argmin() #only go to psi=1

    if data_var == 'NEF3':
        return xdata_1st_time[0:], ydata_1st_time[0:]*1e19
    elif data_var=='TEF3':
        return xdata_1st_time[0:], ydata_1st_time[0:]*1e3
    else:
        return xdata_1st_time, ydata_1st_time


def plot_fits(simulations): 

    # gradient plots
    fig_grad,grad_ax = plt.subplots(ncols=3,nrows=1)
    dp_dx_ax = grad_ax[0]
    dn_dx_ax = grad_ax[1]
    dt_dx_ax = grad_ax[2]

    # fit plots
    fig, profiles_axes = plt.subplots(ncols=2,nrows=2)
    te_axes = profiles_axes[0,0]
    ne_axes = profiles_axes[0,1]
    ti_axes = profiles_axes[1,0]
    pe_axes = profiles_axes[1,1]

    # get the fit data
    
    # this file is fit_data.csv cross ref. against the pedestal DB
    # df_fit_data = pd.read_csv('/work/jsimpson/jetto/python_script/dev_new_plotting_script/read_ppf/fits_peped_nesep_scan_matched_against_ped_db.csv')
    
    # this is the just all the fits which Lorenzo gave me for the peped v. nesep scaling
    df_fit_data = pd.read_csv('/work/jsimpson/jetto/python_script/dev_new_plotting_script/read_ppf/fit_data.csv',skipinitialspace=True)
    df_fit_data.dropna(inplace=True) # gets rid of NaNs
    # printprint(df_fit_data)
    #  filter for the nesep i want
    # df_fit_data = df_fit_data[(df_fit_data['nesep']>1.9) & (df_fit_data['nesep']<2.1)]
    # df_fit_data = df_fit_data[df_fit_data['divertor configuration'] == 'V/V']
    i=0
    cycle = ['r', 'g', 'k', 'b', 'c', 'm', 'orange']
    for index,row in df_fit_data.iterrows():
        # iterate over dataset
        # print(row)
        [dda,user] = row['dda'].split('/')
        low_gas_ppf = '/pulse/'+str(row['shot'])+'/ppf/signal/'+user.strip()+'/'+dda+'/'
        low_gas_ppf_seq_no = '0'
        _, nef = read_sal('NEF3', low_gas_ppf, low_gas_ppf_seq_no)
        _, tef = read_sal('TEF3', low_gas_ppf, low_gas_ppf_seq_no)
        _, psie = read_sal('PSIE', low_gas_ppf, low_gas_ppf_seq_no)
        _, psif = read_sal('PSIF', low_gas_ppf, low_gas_ppf_seq_no)
        if nef.any() is None:
            #     error move on
            continue


        # shift data
        psif,nef,tef=shift(tef,nef,psif,te_at_sep=100)

        ne_min = 2.8e19
        ne_max = 3.2e19
        if nef[-1] < ne_max and nef[-1] > ne_min:
        # for the color iterator
            if i==len(cycle)-1:
                i=0
            else:
                i=i+1
            # print(i)
        #
            nesep_str = str(nef[-1])
            te_axes.plot(psif, tef, label='Pedestal fit nesep='+nesep_str, color=cycle[i],linestyle='dotted')
            ne_axes.plot(psif, nef, label='Pedestal fit nesep='+nesep_str, color=cycle[i], linestyle='dotted')
            pressure =1.6E-19 * np.array(nef) * np.array(tef)
            pe_axes.plot(psif, pressure, label='Pedestal fit nesep='+nesep_str, color=cycle[i], linestyle= 'dotted')


            # Plot the derivatives

            tef_deriv = calc_deriv(psif,tef)
            nef_deriv = calc_deriv(psif,nef)
            pressure = 1.6E-19 * np.array(nef) * np.array(tef)
            pef_deriv = calc_deriv(psif,pressure)

            dp_dx_ax.plot(psif[0:-1], tef_deriv, label='Pedestal fit grad nesep=' + nesep_str, color=cycle[i],linestyle='dotted')

            dn_dx_ax.plot(psif[0:-1], nef_deriv, label='Pedestal fit grad nesep=' + nesep_str, color=cycle[i], linestyle='dotted')

            dt_dx_ax.plot(psif[0:-1], pef_deriv, label='Pedestal fit grad nesep=' + nesep_str, color=cycle[i],linestyle='dotted')

        # plot the profile gradient for the simulations
        for simulation in simulations:
            jsp = simulation['JSP_mishka']
            jsp = jsp.isel(time=-1)
            
            psif = jsp['XPSI']
            tef_deriv = calc_deriv(jsp['XPSI'],jsp['TE'])
            nef_deriv = calc_deriv(jsp['XPSI'],jsp['NE'])
            pef_deriv = calc_deriv(jsp['XPSI'],jsp['PRE'])

            dp_dx_ax.plot(psif[0:-1], tef_deriv,label=simulation.label, color=simulation.color, linestyle=simulation.linestyle)
            dp_dx_ax.set_ylabel('grad(T_e)')
            
            dn_dx_ax.plot(psif[0:-1], nef_deriv, label=simulation.label, color=simulation.color, linestyle=simulation.linestyle)
            dn_dx_ax.set_ylabel('grad(N_e)')

            dt_dx_ax.plot(psif[0:-1], pef_deriv, label=simulation.label, color=simulation.color, linestyle=simulation.linestyle)
            dt_dx_ax.set_ylabel('grad(P_e)')