import networkx as nx
import matplotlib.pyplot as plt
#Draw the network with curved edges ---  FUNCTION
#from matplotlib.patches import FancyArrowPatch, Circle
import numpy as np
from networkx import fast_gnp_random_graph, connected_watts_strogatz_graph

n = 1000 #number of nodes in the graph
G_Rand = connected_watts_strogatz_graph(n,5,1,seed=None)
G_Latt = connected_watts_strogatz_graph(n,5,0,seed=None)
G_SM = connected_watts_strogatz_graph(n,5,0.08,seed=None)
pos = nx.circular_layout(G_Rand)

nx.draw(G_SM,pos,node_size=2,node_color='black',edge_color='k',width=0.4)
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

#That first part was theoretical, now we consider a real resting-state-derived graph and we assess its small-worldness
import networkx as nx
import matplotlib.pyplot as plt
#Draw the network with curved edges ---  FUNCTION
#from matplotlib.patches import FancyArrowPatch, Circle
import numpy as np
from networkx import fast_gnp_random_graph, connected_watts_strogatz_graph

#We want to create a lattice graph and a random graph with the same n as our network. Because we can have isolated nodes, we exclude them
G_SM = G #We copy then network
G.remove_nodes_from(list(nx.isolates(G_SM))) #We remove isolates
n = len(G_SM.nodes)
degree = np.array(G_SM.degree)
mean_degree = np.mean(degree[:,1])
median_degree = int(np.median(degree[:,1])) #I will use the median as K when building regular and random graphs. BUT THIS IS PROBABLY WRONG


G_Rand = connected_watts_strogatz_graph(n,median_degree,1,seed=None)
G_Latt = connected_watts_strogatz_graph(n,median_degree,0,seed=None)
pos = nx.circular_layout(G_SM)
nx.draw(G_SM,pos,node_size=2,node_color='black',edge_color='k',width=0.4)
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
