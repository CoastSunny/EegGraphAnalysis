# Preprocessing

# Loading the data
raw = mne.io.read_raw_eeglab(raw_path, eog=["E125", "E126", "E127", "E128"],
                             preload=True)

# Filtering and referencing
raw.filter(0.1, None, fir_design='firwin')
raw.filter(None, 40., fir_design='firwin')

raw.set_eeg_reference('average', projection=False)  # set EEG average reference

# Remove bad segments, mark bad channels with visual inspection
raw.plot(color=color, n_channels=n_channels, bad_color=bad_color, title=title)

# Bad channels
raw.info['bads'] += [] #or do it using the raw.plot function.
