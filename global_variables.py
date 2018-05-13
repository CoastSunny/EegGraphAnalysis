### Loading the data ###
sbj = "IE008_RC"  # Name of the subject
raw_folder = 'D:/MATLAB/datos nuevos/resting/P1 IMPORT/EC/'
clean_folder = 'D:/MATLAB/datos nuevos/resting/P1 IMPORT/EC/clean/' #folder in which we will save raw cleaned data
epochs_folder = 'D:/MATLAB/datos nuevos/resting/P1 IMPORT/EC/epochs/' #folder in which we will save epochs data
result_folder = 'D:/MATLAB/datos nuevos/resting/P1 IMPORT/EC/results/'
raw_fname = sbj + "_RESTINGEC"  # Subject name should be followed by EO or EC
title = 'Subject: ' + raw_fname
raw_file_ext = '.set'
raw_path = os.path.join(raw_folder, raw_fname + raw_file_ext)

### Global Variables ###
n_channels = 128
n_channels_used = 124
bad_color = 'red'
color = dict(eeg='darkblue', eog='purple', stim='yellow')
tmin = 0.0  # exclude the baseline period
