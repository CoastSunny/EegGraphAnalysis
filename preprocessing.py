# Preprocessing
import mne
from mne import Epochs
import os

### Loading the data ###
sbj = "IE008_RC"  # Name of the subject
raw_folder = 'D:/MATLAB/datos nuevos/resting/P1 IMPORT/EC/'
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

# Filtering
raw.filter(1., None, fir_design='firwin')
raw.filter(None, 30., fir_design='firwin')

raw.set_eeg_reference('average', projection=False)  # set EEG average reference

#Remove bad segments, mark bad channels
raw.plot(color=color, n_channels=n_channels, bad_color=bad_color, title=title)

#Bad channels
raw.info['bads'] += [] #or do it using the raw.plot function.

# Epochs creation. We reject epochs based on previously made annotations
events = mne.make_fixed_length_events(raw, id=1, duration=2)
raw.info['projs'] = []
epochs = Epochs(raw, events, tmin=0, tmax=2, baseline=(None, 0), detrend=1, reject_by_annotation=True)

# Rejection threshold. We will pass this threshold to ICA
reject = get_rejection_threshold(epochs, decim=1)

# ICA for eye movements and eye blinks detection
raw_tmp = raw.copy()
picks = mne.pick_types(raw_tmp.info, eeg=True, eog=True, stim=False, exclude='bads')
ica = mne.preprocessing.ICA(method="extended-infomax", random_state=1, n_components = 25)
ica.fit(raw_tmp, picks=picks, reject=reject)
ica.plot_components(picks=range(25), inst=raw_tmp) #Visual inspection
ica.plot_sources(inst=raw_tmp)

# Advanced artifact detection
from mne.preprocessing import create_eog_epochs
eog_average = create_eog_epochs(raw_tmp, reject=reject,
                                picks=picks).average()
eog_epochs = create_eog_epochs(raw_tmp, reject=reject)  # get single EOG trials
eog_inds, scores = ica.find_bads_eog(eog_epochs)  # find via correlation
ica.plot_scores(scores, exclude=eog_inds)  # look at r scores of components
ica.exclude + = [] # Here you can add the Ica components you found by visual inspection
ica.exclude.extend(eog_inds) # We exclude components found by automatic artifact detection
raw_backup = raw.copy() #We create a raw backup
ica.apply(raw) # We apply ica

#Now we re-create epochs excluding bad epochs
epochs = Epochs(raw, events, tmin=0, tmax=2, baseline=(None, 0), detrend=1, reject_by_annotation=True, reject = reject, preload=True)
epochs.drop_bad()
epochs.interpolate_bads(reset_bads=False,verbose=False)  #We interpolate bad channels
mne.rename_channels(epochs.info,  {'E125' : '_E125','E126':'_E126','E127':'_E127','E128':'_E128'})
picks = mne.pick_types(raw.info, eeg=True, eog=False, stim=False, include = [], exclude=[]) #We want to select all the eeg channels
