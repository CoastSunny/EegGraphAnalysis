# MST metrics and data visualization
# You can plot the connectivity matrix with this function
plot_matrix(con,'PLI')

# Plotting the data
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

# Drawing the network!
#nx.draw(G,pos,node_size=32,node_color='black',edge_color=weights,edge_cmap=plt.cm.Reds) #check how to add edge_vmin properly
#nx.draw(G,pos,node_size=32,node_color='black') #Here we don't consider the threshold
#nx.draw_networkx_labels(G,label_pos,labels,font_size=7,with_labels=True,font_color='grey')
#plt.show()

# Network measures
#centrality = nx.degree_centrality(G)

##################


#Minimum spanning tree
from networkx.algorithms import tree
#We create new weights for the minimum spanning tree (1/weights)
new_weights = []

for i in range(0,len(weights)):
	new_weights.append(1/weights[i]) #Stronger connection will have a shortest distance

new_weights = tuple(new_weights) #convert the list to tuple
#This part does not show the real MST, I have no idea why. I solved it using the maximum spanning tree
#T=nx.minimum_spanning_tree(G,new_weights) #Minimum spanning tree
T = nx.maximum_spanning_tree(G) #This should do extactly the same thing as using w = 1/w as it maximise the distance
nx.draw(T,pos,node_size=32,node_color='black',edge_color='red')
nx.draw_networkx_labels(T,label_pos,labels,font_size=7,with_labels=True,font_color='grey')
plt.show()

# Minimum spanning tree Metrics
#We plot the adjacency matrix
from networkx import adjacency_matrix
A = nx.adjacency_matrix(T)
plot_adjacency_matrix(A)

# We can plot the degree distribution 
plot_degree_distribution(T)
# Metrics list
# Degree, leaf number, betweenness centrality (BC), eccentricity,
# diameter, hierarchy (Th), and degree correlation (R).
from networkx import diameter, eccentricity, betweenness_centrality
#LEAF node
leaf_n = 0
for x in range(0,len(T.edges)):
    if len(T.edges(x)) == 1:
        leaf_n += 1
    print(T.edges(x))
leaf_fraction = leaf_n/n_channels_used #Important values for between subject comparison
print ('Number of leaf nodes: ', leaf_n)
print ('Leaf fraction: ', leaf_fraction)

#Max degree in the MST
max_degree = 0
for i in range(len(T.edges)):
    val = T.degree(i)
    if val > max_degree:
        max_degree = val
print ('Max degree:', max_degree)

#Diameter and eccentricity
nx_diameter = diameter(T, e=None)
print ('Diameter:', nx_diameter)
nx_eccentricity = eccentricity(T, v=None, sp=None)
print ('Eccentricity:', nx_eccentricity)
# Betweenness centrality
nx_btw_centrality = betweenness_centrality(T, k=None, normalized=True, weight=None, endpoints=False, seed=None)
