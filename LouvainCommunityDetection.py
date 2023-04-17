# -*- coding: utf-8 -*-
"""
Plotting the communities produced by the Louvain Community Detection algorithm

@author: Monique Brogan
"""

import networkx as nx
import community as community_louvain
import matplotlib.pyplot as plt
import numpy as np

# import edge file
# https://stackoverflow.com/questions/49683445/create-networkx-graph-from-csv-file

edge_list = open('edge_count.csv', "r")
next(edge_list, None)  # get past the headers
GT = nx.Graph()

G = nx.parse_edgelist(edge_list, delimiter=',', create_using=GT,
                      nodetype=int, data=(('weight', int),))


# Filtering the larger dataset down to the largest component
# Finding the largest component
connected_comps = [G.subgraph(s) for s in nx.connected_components(G)]
print('Sizes of the connected components', [len(c) for c in connected_comps])

largest_component= connected_comps[0]

# creating a subgraph with the largest component
largest_graph = nx.subgraph(G, largest_component)

# run Louvain algorithm on whole graph
partition_full = community_louvain.best_partition(G, weight='weight')
# run Louvain algorithm on largest component
partition = community_louvain.best_partition(largest_graph, weight='weight')

print("# found communities for larger component:", max(partition.values()))

# graph specifications adapted from lectures in Data Science Applications and Techniques, David Weston, Birkbeck University, 2023
pos_discogs = nx.spring_layout(G)
colors2 = [partition.get(node) for node in largest_graph.nodes()]

fig = plt.figure(figsize = (6,6))
cte = 500
# weighted degree normalised to be between 0 and 1, and multiplied by a constant to make the node sizes fit the plot
nsize = np.array([v for ident, v in largest_graph.degree(weight = 'weight')])
nsize = cte*(nsize  - min(nsize))/(max(nsize) - min(nsize))

nodes=nx.draw_networkx_nodes(largest_graph, pos = pos_discogs, cmap = plt.get_cmap('Paired'), node_color = colors2, 
                             node_size = nsize)
edges=nx.draw_networkx_edges(largest_graph, pos = pos_discogs, alpha = .1)
plt.axis('off') 
plt.savefig('./largest_comp.png', dpi = 300, bbox_inches = 'tight')
