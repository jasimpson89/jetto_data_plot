import pandas as pd

def rename_columns(dataframe):
    # Columns are weird names from the headers , rename them
    #Makes it easier to reference in code
    dataframe.rename(columns={'Ip (MA)':'Ip'},inplace=True)
    dataframe.rename(columns={'B (T)':'Bt'},inplace=True)
    dataframe.rename(columns={'P_NBI (MW)':'pnbi'},inplace=True)
    dataframe.rename(columns={'ne separatrix from fit 10^19(m^-3)':'nesep'},inplace=True)
    dataframe.rename(columns={'pe ped height (kPa)':'peped'},inplace=True)
    dataframe.rename(columns={'ne ped height 10^19(m^-3)':'neped'},inplace=True)
    dataframe.rename(columns={'Te ped height (keV)':'teped'},inplace=True)
    dataframe.rename(columns={'average triangularity':'triangularity'},inplace=True)
    dataframe.rename(columns={'P_TOT=PNBI+Pohm+PICRH-Pshi (MW)':'ptot'},inplace=True)
    dataframe.rename(columns={'Te pedestal width Rmid (cm)':'deltate_cm'},inplace=True)
    dataframe.rename(columns={'Ne pedestal width Rmid (cm)':'deltane_cm'},inplace=True)

    return dataframe
def read_ped(file = '',rename_columns_flag = True):
    file = '/Users/jsimpson/work/local/python_scipts/jetto_datadashboard/analysis_routines/pedestal_database_reader/data/Table_EUROfusion_JETILW-JETC_pedestal_v17.txt'
    dataframe = pd.read_csv(file, skipinitialspace=True)

    # rename columns to make them easier to reference
    if rename_columns_flag == True:
        # Allows preservation of column names from the pedestal database
        dataframe = rename_columns(dataframe)

    print(dataframe.columns)
    return dataframe

