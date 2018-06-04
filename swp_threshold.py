import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from networkx import fast_gnp_random_graph, connected_watts_strogatz_graph
min_threshold = 1
max_threshold = 19
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
min_epochs = 1 #Start from epoch n.
n_epochs_touse = 31
max_epochs = min_epochs + n_epochs_touse #End at epoch n.
results = []

# Get the strongest connections
n_con = int((n_channels_used*(n_channels_used-1))/2) # max edges in an undirected graph
min_dist = 0  # exclude sensors that are less than 4cm apart THIS SHOULD BE CHECKED
method = 'pli' # Method used to calculate the connectivity matrix
picks = mne.pick_types(epochs.info, eeg=True, eog=False, stim=False, include = [], exclude=[]) #We want to select all the eeg channels

for step in range(min_threshold,max_threshold+1):
    n_con_touse = int(round(n_con/100*step,0))
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
    threshold = np.sort(con, axis=None)[-n_con_touse]
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

    #We create the graph
    G=nx.Graph()
    for x in range(0, len(idx)):
    	G.add_node(x,pos=(new_loc[x,0],new_loc[x,1])) #I add the nodes to the graph (positions must be re-referenced)
    pos=nx.get_node_attributes(G,'pos')
    con_nodes_new = np.array(con_nodes)

    for x in range(0,len(con_nodes)):
    	G.add_edge(con_nodes_new[x,0],con_nodes_new[x,1], weight=1,alpha=1)  # for weighted networks: weight=con_val[x],alpha=con_val[x])

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

    #We want to create a lattice graph and a random graph with the same n as our network. Because we can have isolated nodes, we exclude them
    G_SM = G
    pos = nx.circular_layout(G)
    #nx.draw(G,pos,node_size=2,node_color='black',edge_color='k',width=0.4)
    #plt.show()
    G_SM.remove_nodes_from(list(nx.isolates(G_SM)))
    graphs = list(nx.connected_component_subgraphs(G_SM)) #There may be more than 1 subgraph. We select the one with more node
    biggest_dimension = 0
    for i in range(0,len(graphs)):
        graph_dimension = len(graphs[i].nodes)
        if graph_dimension > biggest_dimension:
            biggest_graph = i
            biggest_dimension = len(graphs[i].nodes)

    G_SM = graphs[biggest_graph]
    n = len(G_SM.nodes)
    degree = np.array(G_SM.degree)
    mean_degree = np.mean(degree[:,1])
    median_degree = int(np.median(degree[:,1])) #I will use the median as K when building regular and random graphs. BUT THIS IS PROBABLY WRONG
    if median_degree == 3:
        median_degree = 4
    k = median_degree # or int(round(mean_degree,0))
    G_Rand = connected_watts_strogatz_graph(n,k,1,seed=None)
    G_Latt = connected_watts_strogatz_graph(n,k,0,seed=None)
    pos = nx.circular_layout(G_Rand)

    from networkx import average_clustering,  average_shortest_path_length
    c_obs = average_clustering(G_SM, nodes=None, weight=None, count_zeros=True)
    l_obs = average_shortest_path_length(G_SM, weight=None)
    c_rand = average_clustering(G_Rand, nodes=None, weight=None, count_zeros=True)
    l_rand = average_shortest_path_length(G_Rand, weight=None)
    c_latt = average_clustering(G_Latt, nodes=None, weight=None, count_zeros=True)
    l_latt = average_shortest_path_length(G_Latt, weight=None)

    c_obs,l_obs,c_rand,l_rand,c_latt,l_latt

    Dc = (c_latt-c_obs)/(c_latt-c_rand)
    Dl = (l_obs-l_rand)/(l_latt-l_rand)
    from math import sqrt
    SWP = 1 - sqrt((Dc**2 + Dl**2)/2) #small-worldness [1]
    SWP
    print("Graph selected: " + str(biggest_graph) + ", with dimension:" + str(biggest_dimension) + ". The small-worldness propensity is: " + str(round(SWP,3)))
    results.append(SWP)
