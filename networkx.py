import networkx as nx
import matplotlib.pyplot as plt
#Random graph with labels as clustering coefficient
from networkx import fast_gnp_random_graph, connected_watts_strogatz_graph
G = fast_gnp_random_graph(15,0.35,seed=None,directed=False)
cc = nx.clustering(G)
color_map = []
for node in G:
    color_map.append(cc[node])
    cc[node] = "          " + str(round(cc[node],2))

nx.draw(G,node_size=32,node_color='red',edge_color='black',labels = cc)
plt.show()

#regular = 20, 4, 0
#small world = 20,4,0.2
#random = using the next formula
G = connected_watts_strogatz_graph(20,2,0.5,seed=None)
cc = nx.clustering(G)
color_map = []
for node in G:
    color_map.append(cc[node])
    cc[node] = "          " + str(round(cc[node],2))

pos = nx.circular_layout(G)
nx.draw(G,pos,node_size=32,node_color='red',edge_color='black',labels = cc)
plt.show()

from networkx import fast_gnp_random_graph, connected_watts_strogatz_graph
G = fast_gnp_random_graph(15,0.25,seed=None,directed=False)
cc = nx.clustering(G)
color_map = []
for node in G:
    color_map.append(cc[node])
    cc[node] = "          " + str(round(cc[node],2))
pos = nx.circular_layout(G)
nx.draw(G,pos,node_size=32,node_color='red',edge_color='black',labels = cc)
plt.show()
