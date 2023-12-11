import analysis_routines.pedestal_database_reader.read_ped_db as read_ped_db
import pandas as pd


def filter():
    dataframe = pd.read_csv('/home/jsimpson/work/jetto/python_script/jetto_datadashboard/analysis_routines/pedestal_database_reader/data/filtered_2.csv',skipinitialspace=True,converters={'dda': str.strip})

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
    dataframe.rename(columns={'pe pedestal width Rmid (cm)':'deltape_cm'},inplace=True)
    dataframe.rename(columns={'Ne pedestal width (psiN %)': 'deltane_psi'}, inplace=True)
    dataframe.rename(columns={'Te pedestal width (psiN %)': 'deltate_psi'}, inplace=True)
    dataframe.rename(columns={'pe pedestal width (psiN %)': 'deltape_psi'}, inplace=True)
    dataframe.rename(columns={'plasma volume (m^3)':'plasma_volume'},inplace=True)

    return dataframe