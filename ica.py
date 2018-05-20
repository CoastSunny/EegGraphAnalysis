# After visual rejection of bad segments Ica is used to remove artifacts

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

# After visual and automatic inspection you can remove those components
ica.exclude.extend(eog_inds) # We exclude components found by automatic artifact detection
raw_backup = raw.copy() #We create a raw backup
ica.apply(raw) # We apply ica

# Saving the raw file without ICA
cleaned_raw = os.path.join(clean_folder, raw_fname + '-raw.fif')
raw_backup.save(cleaned_raw, overwrite=True)

#We save ICA
cleaned_file = os.path.join(ica_folder, raw_fname + '.fif')
raw.save(cleaned_file, overwrite=True)

# Firstly we load the cleaned data after ica decomposition
cleaned_file = os.path.join(ica_folder, raw_fname + '.fif')
raw = mne.io.read_raw_fif(cleaned_file)
events = mne.make_fixed_length_events(raw, id=1, duration=2)
raw.info['projs'] = []
# Now we re-create epochs excluding bad epochs(
epochs = Epochs(raw, events, tmin=0, tmax=2, baseline=(None, 0), detrend=1, reject_by_annotation=True, reject = reject, preload=True)
epochs.drop_bad()
epochs.interpolate_bads(reset_bads=False,verbose=False)  # We interpolate bad channels
mne.rename_channels(epochs.info,  {'E125' : '_E125','E126':'_E126','E127':'_E127','E128':'_E128'})
picks = mne.pick_types(raw.info, eeg=True, eog=False, stim=False, include = [], exclude=[]) # We want to select all the eeg channels
#We save the epochs
cleaned_epochs= os.path.join(epochs_folder, raw_fname + '-epo.fif')
epochs.save(cleaned_epochs)
