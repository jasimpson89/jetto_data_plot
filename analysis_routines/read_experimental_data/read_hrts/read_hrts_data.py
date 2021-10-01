import numpy as np
from jet.data import sal
import pandas as pd
import matplotlib.pyplot as plt

def read_sal(data_var,part_1,seq_no, time_requested_begin, time_requested_end):

    path = part_1+data_var+':'+seq_no
    print(path)
    data = sal.get(path)
    time = data.dimensions[0].data
    begin_time_idx = (np.abs(time - time_requested_begin)).argmin()
    end_time_idx = (np.abs(time - time_requested_end)).argmin()
    print(time[begin_time_idx])
    # slice data array
    sliced_data = data.data[begin_time_idx:end_time_idx]

    return sliced_data


def read_data(shots,time_begin,time_end):

    # this could be easily set as input parameter

    # df_fit_data = pd.read_csv('../../pedestal_database_reader/data/fit_data.csv',skipinitialspace=True)

    # get HRTS data for every shot
    for shot in  shots:
        part1 = '/pulse/'+str(shot)+'/ppf/signal/jetppf/HRTS/'
        seqno='0'
        te = read_sal('TE',part1,seqno,time_begin,time_end)
        ne = read_sal('NE',part1,seqno,time_begin,time_end)
        error_on_ne = read_sal('DNE',part1,seqno,time_begin,time_end)
        error_on_te = read_sal('TNE',part1,seqno,time_begin,time_end)
        psi = read_sal('PSI',part1,seqno,time_begin,time_end)


    return te, ne, error_on_te, error_on_ne, psi


