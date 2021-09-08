import analysis_routines.pedestal_database_reader.read_ped_db as read_ped_db

"""
THIS FILTERING ROUTINE IS FOR DEC 2020 DATABSE PROVIDED BY LORENZO

THIS LIKELY WILL NEED TO BE UPDATED FOR LATER DATABASES

"""
def plot_pe_nesep():
    df = read_ped_db.read_ped()
    df.columns

    # select shots
    min_shot = 80000
    max_shot = df.shot.max()

    # selected current
    max_current = 2.2
    min_current = 1.8

    # select toroidal field
    max_field = 2.2
    min_field = 1.8

    # selected traiangularity
    # low triangularity
    delta_min = 0.0
    delta_max = 0.35

    # selected P NBI
    lower_nbi = 9
    max_lower = 11

    # Select correct HRTS data. These are needed for the good data
    hrts_flag_A = 1
    hrts_flag_B = 2

    df = df[(df["FLAG: HRTS data validated"] == hrts_flag_A) | (df["FLAG: HRTS data validated"] == hrts_flag_B)]

    selected_peped_nesep = (df[ (df.shot > min_shot) & (df.shot < max_shot) &
                                (df.Ip > min_current) & (df.Ip < max_current) &
                                (df.Bt > min_field) & (df.Bt < max_field) &
                                (df.triangularity > delta_min) & (df.triangularity < delta_max) &
                                (df.pnbi > lower_nbi) & (df.pnbi < max_lower) &
                                (df["FLAG: DEUTERIUM"] == 1)])

    return selected_peped_nesep

