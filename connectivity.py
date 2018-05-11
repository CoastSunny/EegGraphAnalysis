# Resting state Functional Connectivity analysis at the sensor level - Davide Aloi

### Global Variables ###
fmin, fmax = 7.5, 12.5 #theta(3,8) alpha band (7.5,12.5) beta (13,30)
min_epochs = 5 #Start from epoch n.
max_epochs = 25 #End at epoch n.
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
for i, j in zip(ii, jj):
    if linalg.norm(sens_loc[i] - sens_loc[j]) > min_dist:
        con_nodes.append((i, j))
        con_val.append(con[i, j])


con_val = np.array(con_val)


#Plotting the data

G=nx.Graph()
for x in range(0, len(idx)):
	G.add_node(x,pos=(new_loc[x,0],new_loc[x,1])) #I add the nodes to the graph (positions must be re-referenced)

pos=nx.get_node_attributes(G,'pos')
con_nodes_new = np.array(con_nodes)

for x in range(0,len(con_nodes)):
	G.add_edge(con_nodes_new[x,0],con_nodes_new[x,1], weight=con_val[x],alpha=con_val[x])

edges,weights = zip(*nx.get_edge_attributes(G,'weight').items())

plt.figure(figsize=(5, 5))
labels = {} #I create a dictionary with the labels
for x in range (0,len(idx)):
	labels[x] =  idx[x] + 1 #Needed to show the correct electrode label

#Label positions needs to be changed in order to avoid the overlap with electrodes
label_pos = {k:v for k,v in pos.items()}
for i in range(0,len(pos)):
	pos_x = pos[i][0]
	pos_y = pos[i][1]
	upd = {i:[pos_x+0.03,pos_y+0.01]}
	label_pos.update(upd)
