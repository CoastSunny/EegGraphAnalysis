# Resting state Functional Connectivity analysis - Davide Aloi
import mne
from mne import Epochs
import os
import matplotlib.pyplot as plt
import numpy as np
from mne.connectivity import spectral_connectivity
from autoreject import get_rejection_threshold


sbj = "IE008_RC"  # Name of the subject
raw_folder = 'data'
raw_fname = sbj + "_RESTINGEC"  # subject name should be followed by EO or EC
title = 'Subject: ' + raw_fname
raw_file_ext = '.set'
raw_path = os.path.join(raw_folder, raw_fname + raw_file_ext)

# Loading the data
raw = mne.io.read_raw_eeglab(raw_path, eog=["E125", "E126", "E127", "E128"],
                             preload=True)
color = dict(eeg='darkblue', eog='purple', stim='yellow')
n_channels = 128
bad_color = 'red'

# Filtering
raw.filter(1., None, fir_design='firwin')
raw.filter(None, 30., fir_design='firwin')

raw.plot(color=color, n_channels=n_channels, bad_color=bad_color, title=title)

raw.set_eeg_reference('average', projection=False)  # set EEG average reference

# After inspection you can set the bad channels and create the epochs.
# Then we use autoreject to remove epochs with high pick-to-pick amplitude.
events = mne.make_fixed_length_events(raw, id=1, duration=2)
raw.info['projs'] = []
epochs = Epochs(raw, events, tmin=0, tmax=2, baseline=(None, 0), detrend=1)

# Rejection threshold
reject = get_rejection_threshold(epochs, decim=1)

#####
#Here ICA should be implemented


#####

#Now we re-create epochs excluding eog channels
events = mne.make_fixed_length_events(raw, id=1, duration=2)
picks = mne.pick_types(raw.info, eeg=True, eog=True, emg=False, stim=False, exclude='bads')
epochs = Epochs(raw, events, tmin=0., tmax=2, baseline=(None,0), detrend=1, preload=True, picks = picks, reject=reject)
mne.rename_channels(epochs.info,  {'E125' : '_E125','E126':'_E126','E127':'_E127','E128':'_E128'})

#Connectivity
from scipy import linalg
fmin, fmax = 7.5, 12.5 #theta(3,8) alpha band (7.5,12.5) beta (13,30)
sfreq = raw.info['sfreq']  # the sampling frequency
tmin = 0.0  # exclude the baseline period
min_epochs = 15 #Start from epoch n.
max_epochs = 45 #End at epoch n.
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
layout = mne.channels.find_layout(raw.info)
new_loc = layout.pos
# Get the strongest connections
n_con = 130 # show up to 20 connections THIS SHOULD BE CHECKED.
min_dist = 4  # exclude sensors that are less than 4cm apart THIS SHOULD BE CHECKED
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
	labels[x] =  idx[x]

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
