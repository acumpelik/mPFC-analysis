import pandas as pd
import phaselocking_utils
import numpy as np
import bisect
import json

# animal = input('Animal (JC315, JC283, or JC274): ')
# animal = 'JC274'
# session = 'training1'
# day_index = 0 #Following below:
#                 # days_dict = {'JC315': ['20240406', '20240407'], 
#                 #              'JC283': ['20220919', '20220920', '20220921', '20220923'], 
#                 #              'JC274': ['20220312', '20220313', '20220314', '20220315']}

def calculate_cell_stats(animal, session, day_index, arm_number, cell_type):
    #cell_type is pp, pc, p1
    animal_days = {'JC315': 6,
                'JC283': 9, 
                'JC274': 7}


    #Import parameters
    params = pd.read_csv('phaselocking_parameters.csv', header = [0, 1])
    days = params[(animal, 'days')].tolist()
    days = [str(int(i)) for i in days if not pd.isna(i)][animal_days[animal]:]
    num_trials_1 = params[(animal, 'num trials 1')].tolist()
    num_trials_1 = [int(i) for i in num_trials_1 if not pd.isna(i)][animal_days[animal]:]
    tet_par = params[(animal, 'tet par')].tolist()
    tet_par = [int(i) for i in tet_par if not pd.isna(i)][animal_days[animal]:]
    tet_total = params[(animal, 'num tetrodes')].tolist()
    tet_total = [int(i) for i in tet_total if not pd.isna(i)][animal_days[animal]:]

    day = days[day_index]
    tetrode = tet_par[day_index]
    num_tetrodes = tet_total[day_index]



    filepath = animal + '-data/' + animal + '-' + day + '/' + animal + '-' + day + '_' + session #Where the .whl, .clu, etc. are located
    speed_filepath = 'one_drive_data/eight_arm_fig_data_andrea/analysis/' + animal + '-' + day + '/' + animal + '_' + day + '_' + session + '.speed_vladVersion'
        #The speed files, stored in the one drive 
            #Note that speed is set to 0 outside of trials, so this file does not work when the animal is running back in the outer ring
    inst_phase, filtered_eegh = phaselocking_utils.get_phase(filepath, tetrode, num_tetrodes)
    speed_filter = phaselocking_utils.filter_for_speed(speed_filepath)
    peak_filter = phaselocking_utils.peaks_filter(filtered_eegh) 
    res = phaselocking_utils.to_int_list(filepath + '.res')

        
    if res[-1] // 4 > len(filtered_eegh) - 1: #-1 because it's in indices
        print(f'res is longer than eegh: {res[-1] // 4} is longer than {len(filtered_eegh)} in eegh frames (5 kHz).')
        cutoff_index = bisect.bisect_right(res, 4 * (len(filtered_eegh) - 1) + 3) #adding 3 as I use floor division
        print(f'initial max res: {res[-1]}')
        res = res[:cutoff_index]
        print(f'final max res: {res[-1]}')
    res_frames = np.arange(res[-1])

    #Get correct trials
    correct_trials_csv = pd.read_csv('eight_arm_new/Andrea_project/Corrected_behavior_vlad/' + animal + '-' + day + '_' + session + '_data.csv')
        #These .csv files of correct trials corresponding to the .trials files are in the github repository
    correct_trials = correct_trials_csv['CorrectBool'].tolist()
    correct_trials = [bool(val) for val in correct_trials]
    trials_filepath = 'one_drive_data/eight_arm_fig_data_andrea/analysis/' + animal + '-' + day + '/' + animal + '_' + day + '_' + session + '.trials_vladVersion'
        #These files are in the one drive folder

    #Make a filter to keep spikes that happen during correct trials
    with open(trials_filepath, 'r') as file:
        lines = file.readlines()
        trial_timestamps = [line.split() for line in lines]
    timestamps_to_keep = [x for i, x in enumerate(trial_timestamps) if correct_trials[i]]
    correct_filter = [False] * (res[-1] // 512) #the length of the correct filter needs to be res[-1] // 512 in length
    for start, end in timestamps_to_keep:
        for i in range(int(start), int(end) + 1):
            correct_filter[i] = True

    file_ending = '-filter_correct_trials-True-filter_good_cell-Truerate_maps.metrics'
    file_path = 'analysis_Lizzy/analysis/' + animal + '-' + day + '/' + animal + '-' + day + '-' + cell_type + '-' + arm_number + file_ending
        # '-' + cell_type + '-' + rewarded_arm

    # print(file_path)
    data=json.load(open(file_path))


    file = open(animal + '-data/' + animal + '-' + day + '/' + animal + '-' + day + '.des')
    des_raw = file.readlines()
    file.close()
    des = [i.strip('\n') for i in des_raw]
    # print(len(des))

    clusters = [i + 2 for i, x in enumerate(des)]
    clusters_keep = [i for i in clusters if data['good_cell'][i] == 1]

    spatial_info_box = data['spatial_info_box']

    clu = phaselocking_utils.to_int_list(filepath + '.clu')
    a_bars = [] #preferred phase
    r_vals = [] #MVL
    p_vals = []
    for cell in clusters_keep:
        res_for_one_cell = [x for i, x in enumerate(res) if clu[i] == cell]
        res_filtered = [x for x in res_for_one_cell if peak_filter[x // 4] and speed_filter[x // 512]]# eegh_fs = 5kHz and res frames are in 20 kHz
        # avg_freq = len(res_filtered) / (len(time_filtered) / 5_000)
        # if avg_freq >= 0.25: #Keeping only cells with an avg. firing rate of 0.25 Hz across the time kept by all filters
        #         #This criteria is used by Nardin et al., 2023
        #     firing_cell_count += 1
        phases = [inst_phase[i // 4] for i in res_filtered]
        a_bar, r, p_val = phaselocking_utils.stats(phases)
        # if p_val < 0.05:
        a_bars.append(a_bar)
        r_vals.append(r)
        p_vals.append(p_val)
            # selective_cells.append(cell)

    return a_bars, r_vals, p_vals, spatial_info_box

if __name__ == '__main__':
    animal = 'JC274'
    session = 'training1'
    day_index = 1 #Following below:
                # days_dict = {'JC315': ['20240406', '20240407'], 
                #              'JC283': ['20220919', '20220920', '20220921', '20220923'], 
                #              'JC274': ['20220312', '20220313', '20220314', '20220315']}
    rewarded_arms_dict = {'JC315': ['3', '8'], 
                      'JC283': ['7', '2'], 
                      'JC274': ['3', '7', '8']}
    arms = rewarded_arms_dict[animal]
    a_bars, r_vals, p_vals, _ = calculate_cell_stats(animal, session, day_index, arms[0])
    print(a_bars, r_vals, p_vals)