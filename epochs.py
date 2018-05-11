cleaned_epochs= os.path.join(epochs_folder, raw_fname + '.fif')
epochs = mne.read_epochs(cleaned_epochs, proj=True, preload=True, verbose=None)
picks = mne.pick_types(epochs.info, eeg=True, eog=False, stim=False, include = [], exclude=[]) #We want to select all the eeg channels
