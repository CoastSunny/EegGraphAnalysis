#Drawing the network!
nx.draw(G,pos,node_size=32,node_color='black',edge_color=weights,edge_cmap=plt.cm.Reds) #check how to add edge_vmin properly
#nx.draw(G,pos,node_size=32,node_color='black') #Here we don't consider the threshold
nx.draw_networkx_labels(G,label_pos,labels,font_size=7,with_labels=True,font_color='grey')
plt.show()

#Network measures
centrality = nx.degree_centrality(G)

#You can graphically show which are the central nodes
#nx.draw(G,pos,node_color=range(124),node_size=32,cmap=plt.cm.Blues)

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
	new_weights.append(1/weights[i]) #Stronger connection will have a shortest distance

new_weights = tuple(new_weights) #convert the list to tuple
#This part does not show the real MST, I have no idea why. I solved it using the maximum spanning tree
#T=nx.minimum_spanning_tree(G,new_weights) #Minimum spanning tree
T = nx.maximum_spanning_tree(G) #This should do extactly the same thing as using w = 1/w as it maximise the distance
nx.draw(T,pos,node_size=32,node_color='black',edge_color='red')
nx.draw_networkx_labels(T,label_pos,labels,font_size=7,with_labels=True,font_color='grey')
plt.show()

#Minimum spanning tree Metrics
#LEAF node
leaf_n = 0
for x in range(0,123):
    if len(T.edges(x)) == 1:
        leaf_n += 1
    print(T.edges(x))
leaf_fraction = leaf_n/n_channels_used #Important values for between subject comparison
print ('Number of leaf nodes: ', leaf_n)

#Average degree #WORK IN PROGRESS, IT HAS TO BE FIXED
from networkx import average_degree_connectivity
average_degree = average_degree_connectivity(T, source='out', target='out', nodes=None, weight=None)
