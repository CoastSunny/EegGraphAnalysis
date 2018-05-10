# Preprocessing
import mne
from mne import Epochs
import os

### Loading the data ###
sbj = "IE008_RC"  # Name of the subject
raw_folder = 'D:/MATLAB/datos nuevos/resting/P1 IMPORT/EC/'
clean_folder = 'D:/MATLAB/datos nuevos/resting/P1 IMPORT/EC/clean/' #folder in which we will save raw cleaned data
epochs_folder = 'D:/MATLAB/datos nuevos/resting/P1 IMPORT/EC/epochs/' #folder in which we will save epochs data

raw_fname = sbj + "_RESTINGEC"  # Subject name should be followed by EO or EC
title = 'Subject: ' + raw_fname
raw_file_ext = '.set'
raw_path = os.path.join(raw_folder, raw_fname + raw_file_ext)

### Global Variables ###
n_channels = 128
bad_color = 'red'
color = dict(eeg='darkblue', eog='purple', stim='yellow')
tmin = 0.0  # exclude the baseline period

# Loading the data
raw = mne.io.read_raw_eeglab(raw_path, eog=["E125", "E126", "E127", "E128"],
                             preload=True)

# Filtering and referencing
raw.filter(1., None, fir_design='firwin')
raw.filter(None, 30., fir_design='firwin')

raw.set_eeg_reference('average', projection=False)  # set EEG average reference

#Remove bad segments, mark bad channels with visual inspection
raw.plot(color=color, n_channels=n_channels, bad_color=bad_color, title=title)

#Bad channels
raw.info['bads'] += [] #or do it using the raw.plot function.
