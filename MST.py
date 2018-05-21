# MST metrics and data visualization
# You can plot the connectivity matrix with this function
results_band =  os.path.join(result_folder,sbj + '/' + band_considered)

plot_matrix(con,'PLI')

# Creating the graph derived from the matrix
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

# Connectivity strength analysis
mean_connectivity = np.mean(con)
# Connectivity strength in a sub-avareage of electrodes (frontal, occipital, temporal and parietal)
# To be implemented

#Minimum spanning tree
from networkx.algorithms import tree
T = nx.maximum_spanning_tree(G) #This should do extactly the same thing as using w = 1/w as it maximise the distance
nx.draw(T,pos,node_size=32,node_color='black',edge_color='red')
nx.draw_networkx_labels(T,label_pos,labels,font_size=7,with_labels=True,font_color='grey')
plt.show()

# Minimum spanning tree Metrics
# Metrics list
# Degree, leaf number, betweenness centrality (BC), eccentricity,
# diameter, hierarchy (Th), and degree correlation (R).
degree = np.array(T.degree)
mean_degree = np.mean(degree[:,1])
median_degree = np.median(degree[:,1])

#Hubs list:all the nodes with degree > median could be considered as hubs. (Mike X Cohen, Analyzing neural time series data, 2016)
hubs = np.where( degree[:,1] > median_degree )
n_hubs = len(hubs[0])

#We plot the adjacency matrix
from networkx import adjacency_matrix
A = nx.adjacency_matrix(T)
links = len(T.edges)

#Leaf number and leaf fraction
from networkx import diameter, eccentricity, betweenness_centrality
#LEAF node
leaf_n = 0
for x in range(0,len(T.edges)):
    if len(T.edges(x)) == 1:
        leaf_n += 1
    print(T.edges(x))
leaf_fraction = leaf_n/len(T.nodes) #Important values for between subject comparison

#Max degree in the MST
max_degree = 0
for i in range(len(T.edges)):
    val = T.degree(i)
    if val > max_degree:
        max_degree = val

#Diameter and eccentricity
nx_diameter = diameter(T, e=None)
nx_eccentricity = eccentricity(T, v=None, sp=None)
nx_eccentricity_mean = np.mean(nx_eccentricity[:,1]) #whole MST eccentricity
# Betweenness centrality (BC) and BCmax
nx_btw_centrality = betweenness_centrality(T, k=None, normalized=True, weight=None, endpoints=False, seed=None)
nx_btw_centrality_mean = np.mean(nx_btw_centrality[:,1]) 
# Applying round to the betweenness centrality to show only the first 3 values

nx_btw_max = 0
for i in range(len(T.edges)):
    val = nx_btw_centrality[i]
    if val > nx_btw_max:
        nx_btw_max = val

#Tree hierarchy (Th=L/(2mBCmax))
nx_th = leaf_n/(2*links*nx_btw_max) #TO BE CHECKED

# Degree correlation
from networkx import  degree_pearson_correlation_coefficient
nx_d = degree_pearson_correlation_coefficient(T, weight=None, nodes=None)

#### Printing and plotting all the measures #####
plot_adjacency_matrix(A)
# We can plot the degree distribution
plot_degree_distribution(T)

print('Subject: ', title)
print('Band: ', bands)
print('Number of nodes: ', len(T.nodes), ' Number of edges: ', len(T.edges))
print ('Number of hubs', n_hubs)
print ('Averaged PLI:', mean_connectivity)
print ('Number of leaf nodes: ', leaf_n)
print ('Leaf fraction: ', leaf_fraction)
print ('Max degree:', max_degree)
print ('Diameter:', nx_diameter)
print ('Eccentricity:', nx_eccentricity)
print ('Betweenness centrality: ', nx_btw_centrality,2)
print ('Max BC:', nx_btw_max)
print('Tree hierarchy: ', nx_th)
print('Degree correlation: ', nx_d)
