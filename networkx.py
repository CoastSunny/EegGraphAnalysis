import networkx as nx
import matplotlib.pyplot as plt
#Random graph with labels as clustering coefficient
G = fast_gnp_random_graph(5,0.85,seed=None,directed=False)
cc = nx.clustering(G)
color_map = []
for node in G:
    color_map.append(cc[node])
    cc[node] = round(cc[node],3

nx.draw(G,node_size=32,node_color='red',edge_color='black',labels = cc)
plt.show()
