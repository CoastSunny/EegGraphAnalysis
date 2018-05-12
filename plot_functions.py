#Easy way to plot the connectivity matrix
def plot_matrix(con,method):
    import numpy as np
    import matplotlib.pyplot as plt
    r_con = con + con.T - np.diag(np.diag(con)) #I reflect the matrix
    plt.imshow(r_con);
    clb = plt.colorbar()
    clb.ax.set_title(method)
    plt.xlabel('Channels')
    plt.show()
    return
#####################

#Plot the adjacency matrix
def plot_adjacency_matrix(A):
    import numpy as np
    import matplotlib.pyplot as plt
    A = A.todense()
    plt.imshow(A);
    plt.xlabel('Channels')
    plt.show()
    return

#Drawing the network as a circular network to show small-world organization
def draw_smallworld(G,labels,weights):
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
    return
#####################
def plot_degree_distribution (G):
    import collections
    degree_sequence = sorted([d for n, d in G.degree()], reverse=True)  # degree sequence
    # print "Degree sequence", degree_sequence
    degreeCount = collections.Counter(degree_sequence)
    deg, cnt = zip(*degreeCount.items())
    fig, ax = plt.subplots()
    plt.bar(deg, cnt, width=0.80, color='b')
    plt.title("Degree Histogram")
    plt.ylabel("Count")
    plt.xlabel("Degree")
    ax.set_xticks([d + 0.4 for d in deg])
    ax.set_xticklabels(deg)
    # draw graph in inset
    plt.axes([0.4, 0.4, 0.5, 0.5])
    Gcc = sorted(nx.connected_component_subgraphs(G), key=len, reverse=True)[0]
    pos = nx.spring_layout(G)
    plt.axis('off')
    nx.draw_networkx_nodes(G, pos, node_size=20)
    nx.draw_networkx_edges(G, pos, alpha=0.4)
    plt.show()
    return
