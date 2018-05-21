# Resting state Functional Connectivity analysis at the sensor level - Davide Aloi
### Global Variables ###
delta = 0.5,4
alpha = 8,13
theta = 4,8
beta = 13,30
gamma = 30,70
fmin, fmax = alpha
bands = fmin,fmax
band_considered = 'alpha'
min_epochs = 5 #Start from epoch n.
max_epochs = 31 #End at epoch n.
# Get the strongest connections
n_con = 124*123 # show up to n_con connections THIS SHOULD BE CHECKED.
min_dist = 3  # exclude sensors that are less than 4cm apart THIS SHOULD BE CHECKED
method = 'pli' # Method used to calculate the connectivity matrix

#Connectivity
from scipy import linalg
sfreq = epochs.info['sfreq']  # the sampling frequency
con, freqs, times, n_epochs, n_tapers = spectral_connectivity(
    epochs[min_epochs:max_epochs], method=method, mode='multitaper', sfreq=sfreq, fmin=fmin, fmax=fmax,
    faverage=True, tmin=tmin, mt_adaptive=False, n_jobs=1)

# the epochs contain an EOG channel, which we remove now
ch_names = epochs.ch_names
idx = [ch_names.index(name) for name in ch_names if name.startswith('E')]
con = con[idx][:, idx]
# con is a 3D array where the last dimension is size one since we averaged
# over frequencies in a single band. Here we make it 2D

con = con[:, :, 0] #This connectivity matrix can also be visualized

# Plot the sensor locations
sens_loc = [epochs.info['chs'][picks[i]]['loc'][:3] for i in idx]
sens_loc = np.array(sens_loc)
#Layout
layout = mne.channels.find_layout(epochs.info, exclude=[])
new_loc = layout.pos
threshold = np.sort(con, axis=None)[-n_con]
ii, jj = np.where(con >= threshold)

# Remove close connections
con_nodes = list()
con_val = list()
connections_found = 0
for i, j in zip(ii, jj):
    if linalg.norm(sens_loc[i] - sens_loc[j]) > min_dist:
        con_nodes.append((i, j))
        con_val.append(con[i, j])
        connections_found = connections_found + 1

con_val = np.array(con_val)
