# Connectivity strength analysis
r_con = con + con.T - np.diag(np.diag(con)) #I reflect the matrix to correctly calculate all the connectivity strength values
mean_connectivity = round(np.mean(r_con),4)

# Connectivity strength in a sub-avareage of electrodes (frontal, occipital, temporal and parietal)
# To be implemented


lt_picks = mne.epochs.pick_types(epochs_backup.info, eeg=True, eog=False, stim=False, selection=left_temporal) #left_temporal electrodes and so forth
rt_picks = mne.epochs.pick_types(epochs_backup.info, eeg=True, eog=False, stim=False, selection=right_temporal)
lp_picks = mne.epochs.pick_types(epochs_backup.info, eeg=True, eog=False, stim=False, selection=left_parietal)
rp_picks = mne.epochs.pick_types(epochs_backup.info, eeg=True, eog=False, stim=False, selection=left_parietal)
lo_picks = mne.epochs.pick_types(epochs_backup.info, eeg=True, eog=False, stim=False, selection=left_occipital)
ro_picks = mne.epochs.pick_types(epochs_backup.info, eeg=True, eog=False, stim=False, selection=right_occipital)
lf_picks = mne.epochs.pick_types(epochs_backup.info, eeg=True, eog=False, stim=False, selection=left_frontal)
rf_picks = mne.epochs.pick_types(epochs_backup.info, eeg=True, eog=False, stim=False, selection=right_frontal)
