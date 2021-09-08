# Package imports
import analysis_routines.pedestal_database_reader.filter_pe_nesep as filter_pe_nesep

# Std imports
import pandas as pd
import matplotlib.pyplot as plt


def read_samuli_data():

    file = '/Users/jsimpson/work/local/python_scipts/jetto_datadashboard/analysis_routines/pedestal_database_reader/data/summary_sc_runs_sauter.csv'
    dataframe = pd.read_csv(file, skipinitialspace=True)
    return dataframe

def main():

    # Lorenzo pedestal database
    # returns dataframe
    pe_nesep_exp_df = filter_pe_nesep.plot_pe_nesep()

    # Dataframe for Samuli's data
    stability_df = read_samuli_data()


    # get values of stability df that are in experimental datbase, and merge
    # Makes one dataframe which has the experimental data and the stabiltiy data

    pe_nesep_exp_stability_filter_df = pd.merge(pe_nesep_exp_df,stability_df,on=['shot'],how='inner')
    return pe_nesep_exp_df,stability_df,pe_nesep_exp_stability_filter_df