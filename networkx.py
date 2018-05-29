import networkx as nx
import matplotlib.pyplot as plt
#Draw the network with curved edges ---  FUNCTION
from matplotlib.patches import FancyArrowPatch, Circle
import numpy as np

def draw_network(G,pos,ax,sg=None,rad=-0.2):
    for n in G:
        c=Circle(pos[n],radius=0.02,alpha=0.5)
        ax.add_patch(c)
        G.node[n]['patch']=c
        x,y=pos[n]
    seen={}
    for (u,v,d) in G.edges(data=True):
        n1=G.node[u]['patch']
        n2=G.node[v]['patch']
        rad=rad
        if (u,v) in seen:
            rad=seen.get((u,v))
            rad=(rad+np.sign(rad)*0.1)*-1
        alpha=0.5
        color='black'

        e = FancyArrowPatch(n1.center,n2.center,patchA=n1,patchB=n2,
                            arrowstyle='-',
                            connectionstyle='arc3,rad=%s'%rad,
                            mutation_scale=10.0,
                            lw=2,
                            alpha=alpha,
                            color=color)
        seen[(u,v)]=rad
        ax.add_patch(e)
    return e
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
#small world = 20, 4, 0.2/0.5
#random = 20, 4, 1
G = connected_watts_strogatz_graph(20,4,1,seed=None)
cc = nx.clustering(G)
color_map = []
for node in G:
    color_map.append(cc[node])
    cc[node] = "          " + str(round(cc[node],2))

pos = nx.circular_layout(G)
nx.draw(G,pos,node_size=28,node_color='black',edge_color='black') #labels = cc
plt.show()


ax=plt.gca()
draw_network(G,pos,ax,rad=-0.2)
ax.autoscale()
plt.axis('equal')
plt.axis('off')
#plt.savefig("graph.pdf")
plt.show()
