import pandas as pd
import numpy as np
def get_column_names(file):
    file = open(file,'r')
    lines = file.readlines()
    # column lines
    line0 = lines[0]

    # this is the
    split = list(filter(None, line0.split('\t')))
    # clean up
    split_strip = [i.strip() for i in split]
    columns = ['shot','t1','t2']+split_strip[2:len(split_strip)]
    return columns


def read_db(file):
    # this doesn't read the column headers because they are formatted wrong
    dataframe = pd.read_csv(file,delim_whitespace=True,skiprows=1,header=None)
    return dataframe

def rename_columns(dataframe):
    # Columns are weird name from the headers , rename this
    dataframe.rename(columns={'Ip (MA)':'Ip'},inplace=True)
    dataframe.rename(columns={'B (T)':'Bt'},inplace=True)
    dataframe.rename(columns={'P_NBI (MW)':'pnbi'},inplace=True)
    dataframe.rename(columns={'separatrix n_e 10^19(m^-3)':'nesep'},inplace=True)
    dataframe.rename(columns={'pe ped height pre-ELM (kPa)':'peped'},inplace=True)
    dataframe.rename(columns={'ne ped height pre-ELM  10^19(m^-3)':'neped'},inplace=True)
    dataframe.rename(columns={'Te ped height pre-ELM (keV)':'teped'},inplace=True)
    dataframe.rename(columns={'P_tot (MW)':'ptot'},inplace=True)

    return dataframe
def read_ped(file = '',rename_columns_flag = True):
    file = '/Users/jsimpson/work/local/python_scipts/pedestal_db_reader/table_EUROfusion_db_JSimpson_24april2019_D_withpellets_normp_nokikcs_only_validated.dat'
    dataframe = read_db(file)
    columns = get_column_names(file)
    dataframe.columns = columns

    # rename columns to make them easier to reference
    if rename_columns_flag == True:
        # Allows preservation of column names from the pedestal database
        dataframe = rename_columns(dataframe)

    if len(columns) != len(dataframe.iloc[0,:]):
        import sys
        print('Column and data length different. Column length = ', len(columns),
                 ' row length = ', len(dataframe.iloc[0,:]))
        sys.exit()
    print(dataframe.columns)
    return dataframe

