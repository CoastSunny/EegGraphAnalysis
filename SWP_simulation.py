#References
#[1] Muldoon et al., 2016
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from networkx import fast_gnp_random_graph, connected_watts_strogatz_graph
from networkx import average_clustering,  average_shortest_path_length

n = 1000 #number of nodes in the graph
k = 5
results = []

for x in range(1,10001):
    i = x/10000
    G_Rand = connected_watts_strogatz_graph(n,k,1,seed=None)
    G_Latt = connected_watts_strogatz_graph(n,k,0,seed=None)
    G_SM = connected_watts_strogatz_graph(n,k,i,seed=None)
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
    result.append(SWP)
