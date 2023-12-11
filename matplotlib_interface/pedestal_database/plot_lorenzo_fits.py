from jet.data import sal
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

"""
This plots fits from Lorenzo's mtanh fits from teh a csv file which I created 

this csv is matched with peped v. nesep trend 

"""

def shift(te,ne,xaxis,te_at_sep = 100):

    # find the 100 eV point first

    idx_at_tesep = (np.abs(te-te_at_sep).argmin()) + 1 # so include the 100 eV point
    x_at_tesep = xaxis[idx_at_tesep]

    shifted_te_profile = te[0:idx_at_tesep]
    shifted_ne_profile = ne[0:idx_at_tesep]
    shifted_x_axis = np.linspace(0,1,len(xaxis[0:idx_at_tesep]))
    # print(len(shifted_te_profile),len(shifted_x_axis))
    return shifted_x_axis, shifted_ne_profile,shifted_te_profile, idx_at_tesep
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
    # print(path)
    try:
        data = sal.get(path)
    except:
        print('Error with PPF reading of {ppf}'.format(ppf=path))
        # this is a bad way of handling this
        return np.array(None), np.array(None)

    try:
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
    except IndexError:
        # asking for a scalar from the PPF

        return None, data.data[0]


def plot_fits(simulations, opts, ne_width_ax, te_width_ax):

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

    # Temporary addition for confied region plots 
    fig_conf, [confined_region_psi,confined_region_psi_te]  = plt.subplots(ncols=2,nrows=1)
    confined_region_density_width = []
    confined_region_density_width_te = []
    confined_region_density_width_nesep = []

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
        _, rmid = read_sal('RMDF', low_gas_ppf, low_gas_ppf_seq_no)
        # density pedestal height
        _, mtanh_neped = read_sal('HN3', low_gas_ppf, low_gas_ppf_seq_no)
        # temperature pedestal height
        _, mtanh_teped = read_sal('HT5', low_gas_ppf, low_gas_ppf_seq_no)
        
        
        if nef.any() is None:
            #     error move on
            continue


        # shift data
        psif,nef,tef, shift_idx =shift(tef,nef,psif,te_at_sep=100)
        rshift = rmid[0:shift_idx]
        # calculate density width within confined plasma
        idx_neped = (np.abs(nef-(mtanh_neped*1e19))).argmin()
        idx_teped = (np.abs(tef - (mtanh_teped * 1e3))).argmin()

        if opts.x == 'psi':
            # psi width
            confined_region_density_width.append(psif[-1] - psif[idx_neped])
            confined_region_density_width_te.append(psif[-1] - psif[idx_teped])
        else:
            confined_region_density_width.append(rshift[-1] - rshift[idx_neped])
            confined_region_density_width_te.append(rshift[-1] - rshift[idx_teped])


        confined_region_density_width_nesep.append(nef[-1])

        print('#####################')
        print('nesep = ', str(nef[-1]))
        print('width = ', str(psif[-1] - psif[idx_neped]))
        print('ppf - ', low_gas_ppf)

        ne_min = opts.nesep_request*1e19*0.8
        ne_max = opts.nesep_request*1e19*1.2
        ne_min=0
        ne_max=10e19
        if nef[-1] < ne_max and nef[-1] > ne_min:
        # for the color iterator
            if i==len(cycle)-1:
                i=0
            else:
                i=i+1
            # print(i)
        #
            nesep_str = str(nef[-1])
            te_axes.plot(psif, tef, color=cycle[i],linestyle='dotted')
            ne_axes.plot(psif, nef, color=cycle[i], linestyle='dotted')
            pressure =1.6E-19 * np.array(nef) * np.array(tef)
            pe_axes.plot(psif, pressure, color=cycle[i], linestyle= 'dotted')


            # Plot the derivatives

            tef_deriv = calc_deriv(psif,tef)
            nef_deriv = calc_deriv(psif,nef)
            pressure = 1.6E-19 * np.array(nef) * np.array(tef)
            pef_deriv = calc_deriv(psif,pressure)

            dp_dx_ax.plot(psif[0:-1], tef_deriv, color=cycle[i],linestyle='dotted')

            dn_dx_ax.plot(psif[0:-1], nef_deriv, color=cycle[i], linestyle='dotted')

            dt_dx_ax.plot(psif[0:-1], pef_deriv, color=cycle[i],linestyle='dotted')

            print('/pulse/'+str(row['shot'])+'/ppf/signal/'+user.strip()+'/'+dda+'/')

        # plot the profile gradient for the simulations and the profiles on the 
        for simulation in simulations:
            jsp = simulation['JSP_mishka']
            jsp = jsp.isel(time=-1)
            jst = simulation["JST_mishka"].isel(time=-1)


            psif = jsp['XPSI']
            tef_deriv = calc_deriv(jsp['XPSI'],jsp['TE'])
            nef_deriv = calc_deriv(jsp['XPSI'],jsp['NE'])
            pef_deriv = calc_deriv(jsp['XPSI'],jsp['PRE'])

            # Profile plots on the mtanh fits 
            te_axes.plot(psif, jsp['TE'], label=simulation.label, color=simulation.color,linestyle=simulation.linestyle,linewidth=1.0)
            ne_axes.plot(psif, jsp['NE'], label=simulation.label, color=simulation.color, linestyle=simulation.linestyle,linewidth=1.0)     
            pe_axes.plot(psif, jsp['PRE'], label=simulation.label, color=simulation.color, linestyle=simulation.linestyle,linewidth=1.0)



            # Gradient plots
            dp_dx_ax.plot(psif[0:-1], tef_deriv,label=simulation.label, color=simulation.color, linestyle=simulation.linestyle)
            dp_dx_ax.set_ylabel('grad(T_e)')
            
            dn_dx_ax.plot(psif[0:-1], nef_deriv, label=simulation.label, color=simulation.color, linestyle=simulation.linestyle)
            dn_dx_ax.set_ylabel('grad(N_e)')

            dt_dx_ax.plot(psif[0:-1], pef_deriv, label=simulation.label, color=simulation.color, linestyle=simulation.linestyle)
            dt_dx_ax.set_ylabel('grad(P_e)')

            # Pedestal width in psi
            psi = jsp['XPSI'].values
            nesep = ((jsp['NE'])[-1]).values
            pedestal_width_psi = psi[-1] - psi[int(jst['JTOB'])]

            confined_region_psi.plot(nesep,pedestal_width_psi,label=simulation.label, color=simulation.color,marker=simulation.marker)

    # Make a scatter plot for the confied plasma widht 
    ne_width_ax.scatter(np.array(confined_region_density_width_nesep)/1e19,confined_region_density_width,marker='*',color='r',alpha=0.3)
    te_width_ax.scatter(np.array(confined_region_density_width_nesep)/1e19,confined_region_density_width_te,marker='*',color='r',alpha=0.3)

    return  confined_region_density_width_nesep, confined_region_density_width, confined_region_density_width_te