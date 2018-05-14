cleaned_epochs= os.path.join(epochs_folder, raw_fname + '-epo.fif')
epochs = mne.read_epochs(cleaned_epochs, proj=True, preload=True, verbose=None)
picks = mne.pick_types(epochs.info, eeg=True, eog=False, stim=False, include = [], exclude=[]) #We want to select all the eeg channels
epochs.plot()
# After an ulterior visual inspection you can save the epochs again
epochs.save(cleaned_epochs)



#You can plot some information
epochs.plot_psd(fmin=1., fmax=35.)
epochs.plot_psd_topomap(ch_type='eeg', normalize=True)
