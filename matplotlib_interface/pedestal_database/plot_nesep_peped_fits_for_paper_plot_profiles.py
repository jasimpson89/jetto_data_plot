from jet.data import sal
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plot_nesep_peped_fits



def plot_fit():
    low_gas_ppf = '/pulse/82447/ppf/signal/rfrid/T001/'
    low_gas_ppf_seq_no = '0'
    _, nef = plot_nesep_peped_fits.read_sal('NEF3', low_gas_ppf, low_gas_ppf_seq_no)
    _, tef = plot_nesep_peped_fits.read_sal('TEF3', low_gas_ppf, low_gas_ppf_seq_no)
    _, psif = plot_nesep_peped_fits.read_sal('PSIF', low_gas_ppf, low_gas_ppf_seq_no)
    psif,nef,tef, shift_idx =plot_nesep_peped_fits.shift(tef,nef,psif,te_at_sep=100)

    pressure = (nef*tef*1.6e-19)/1e3

    return pressure