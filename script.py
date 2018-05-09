# Resting state Functional Connectivity analysis at the sensor level - Davide Aloi
import mne
from mne import Epochs
import os
import matplotlib.pyplot as plt
import numpy as np
from mne.connectivity import spectral_connectivity
from autoreject import get_rejection_threshold

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
fmin, fmax = 7.5, 12.5 #theta(3,8) alpha band (7.5,12.5) beta (13,30)
min_epochs = 5 #Start from epoch n.
max_epochs = 25 #End at epoch n.
# Get the strongest connections
n_con = 200 # show up to n_con connections THIS SHOULD BE CHECKED.
min_dist = 3  # exclude sensors that are less than 4cm apart THIS SHOULD BE CHECKED

# Loading the data
raw = mne.io.read_raw_eeglab(raw_path, eog=["E125", "E126", "E127", "E128"],
                             preload=True)

# Filtering
raw.filter(1., None, fir_design='firwin')
raw.filter(None, 30., fir_design='firwin')

raw.set_eeg_reference('average', projection=False)  # set EEG average reference

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

#Connectivity
from scipy import linalg
sfreq = raw.info['sfreq']  # the sampling frequency
con, freqs, times, n_epochs, n_tapers = spectral_connectivity(
    epochs[min_epochs:max_epochs], method='pli', mode='multitaper', sfreq=sfreq, fmin=fmin, fmax=fmax,
    faverage=True, tmin=tmin, mt_adaptive=False, n_jobs=1)

# the epochs contain an EOG channel, which we remove now
ch_names = epochs.ch_names
idx = [ch_names.index(name) for name in ch_names if name.startswith('E')]
con = con[idx][:, idx]
# con is a 3D array where the last dimension is size one since we averaged
# over frequencies in a single band. Here we make it 2D
con = con[:, :, 0]

# Plot the sensor locations
sens_loc = [raw.info['chs'][picks[i]]['loc'][:3] for i in idx]
sens_loc = np.array(sens_loc)
#Layout
layout = mne.channels.find_layout(raw.info, exclude=[])
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
import plotly.plotly as py
from plotly.graph_objs import *
import networkx as nx

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

#Drawing the network!
nx.draw(G,pos,node_size=32,node_color='black',edge_color=weights,edge_cmap=plt.cm.Reds) #check how to add edge_vmin properly
#nx.draw(G,pos,node_size=32,node_color='black') #Here we don't consider the threshold

nx.draw_networkx_labels(G,label_pos,labels,font_size=7,with_labels=True,font_color='grey')
plt.show()

#Network measures
centrality = nx.degree_centrality(G)
####Just an example, many measures can be added (path length, betweenness and so forth)

##################
#Drawing the network as a circular network to show small-world organization
sm_w = G
pos_c=nx.circular_layout(sm_w)
#Label positions needs to be changed in order to avoid the overlap with electrodes
label_pos_c = {k:v for k,v in pos_c.items()}
for i in range(0,len(pos_c)):
	pos_x = pos_c[i][0]
	pos_y = pos_c[i][1]
	upd = {i:[pos_x+0.03,pos_y+0.01]}
	label_pos_c.update(upd)

nx.draw(sm_w,pos_c,node_size=32,node_color='black',edge_color=weights,edge_cmap=plt.cm.Reds) #check how to add edge_vmin properly
nx.draw_networkx_labels(sm_w,label_pos_c,labels,font_size=7,with_labels=True,font_color='grey')
plt.show()
#####################

#Minimum spanning tree
from networkx.algorithms import tree
#We create new weights for the minimum spanning tree (1/weights)
new_weights = []
for i in range(0,len(weights)):
	w = 1/weights[i] #Stronger connection will have a shortest distance
	new_weights.append(w)
new_weights = tuple(new_weights) #convert the list to tuple

T=nx.minimum_spanning_tree(G,new_weights) #Minimum spanning tree

nx.draw(T,pos,node_size=32,node_color='black',edge_color='red')
nx.draw_networkx_labels(T,label_pos,labels,font_size=7,with_labels=True,font_color='grey')
plt.show()

#Minimum spanning tree as spring
