# Preprocessing

# Loading the data
raw = mne.io.read_raw_eeglab(raw_path, eog=["E125", "E126", "E127", "E128"],
                             preload=True)

# Filtering and referencing
raw.filter(0.1, None, fir_design='firwin')
raw.filter(None, 80., fir_design='firwin')
raw.notch_filter(50)
raw.set_eeg_reference('average', projection=False)  # set EEG average reference

# Remove bad segments, mark bad channels with visual inspection
raw.plot(color=color, n_channels=n_channels, bad_color=bad_color, title=title)

# Bad channels
#This can give you an idea of which electrodes could be outliers
data, times = raw[picks, :]
picks = mne.pick_types(raw.info, meg=False, eeg=True)
outliers = is_outlier(data, 3.0);
#With this function I list all the electrods that are supposed to be outliers
for x in range(0, len(outliers)):
	if outliers[x] == 1:
		print ("Outlier Electrode detected:", x+1)
