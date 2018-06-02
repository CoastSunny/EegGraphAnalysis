import networkx as nx
import matplotlib.pyplot as plt
#Draw the network with curved edges ---  FUNCTION
from matplotlib.patches import FancyArrowPatch, Circle
import numpy as np

from networkx import fast_gnp_random_graph, connected_watts_strogatz_graph
G_Rand = connected_watts_strogatz_graph(300,4,1,seed=None)
G_Latt = connected_watts_strogatz_graph(300,4,0,seed=None)
G_SM = connected_watts_strogatz_graph(300,4,0.05,seed=None)
pos = nx.circular_layout(G_Rand)

nx.draw(G_SM,pos,node_size=25,node_color='red',edge_color='black')
plt.show()

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
#References
#[1] Muldoon et al., 2016
