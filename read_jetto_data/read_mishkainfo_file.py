import numpy as np
import xarray as xr
import os
def read_info_file(run_dir):
    # Open MISHKAinstabilities.info file
    file_path = run_dir+'/MISHKAinstabilities.info'
    infofile  = open(file_path, 'r')

    # stores block information
    unstable_mode_number=[]
    unstable_growth_rate = []
    time = []

    # Stores the most unstable mode and growth rate for a particular time
    most_unstable_mode = []
    most_unstable_mode_time = []
    most_unstable_mode_growth_rate = []


    xr_Data = []
    lines = infofile.readlines()
    block_found = False
    started_block = False
    for line in lines:
        if line.find('PREALOC') > -1:
            # Found a block
            block_found = True
            # save time , always at the end of the string
            split = line.split()
            # we need to save this so that we can save the xarray properly

            time_split = float(split[-1])
            time.append(time_split)
        if block_found == True:
            # first check if we have hit the end of the block
            if line.find('PREALOC') > -1 and started_block == True:

                block_found = False
                if unstable_growth_rate != [] and unstable_mode_number != []:

                    # were already into the next block so get the time of the block this data refers too if not the first block
                    if len(time) > 1:
                        time_xr = time[-2]
                    else:
                        time_xr = time[0]

                    idx_most_unstable_growth_rate = (np.array(unstable_growth_rate)).argmax()
                    most_unstable_mode_growth_rate.append(unstable_growth_rate[idx_most_unstable_growth_rate])
                    most_unstable_mode.append(unstable_mode_number[idx_most_unstable_growth_rate])
                    most_unstable_mode_time.append(time_xr)

                # reintiliase ready for the next block of data
                # A block of data is defined as a single time, containing many mode numbers which are associated with a
                # growth rate (and other properties which could be saved)
                unstable_mode_number = []
                unstable_growth_rate = []
                started_block = False
            # not at end of block, if block found is still true
            if block_found == True:
                split = line.split()
                # found an unstable mode
                if split[-1].find('T') >-1:
                    started_block = True
                    unstable_growth_rate.append(float( split[9]))
                    unstable_mode_number.append(float(split[1])*-1)  # some reason the file stores the instabilites as -MODE_NO



    if most_unstable_mode == []:
        # Empty and can't add in
        return None

    return xr.DataArray(most_unstable_mode,dims=["time"], coords={"time":most_unstable_mode_time})

