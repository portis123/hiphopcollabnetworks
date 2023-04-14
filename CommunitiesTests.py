# -*- coding: utf-8 -*-
"""
Created on Thu Apr  6 11:16:38 2023

Running Louvain and Leiden algorithms and comparing modularity scores

@author: Monique Brogan
"""
import networkx as nx

# import edge file
# https://stackoverflow.com/questions/49683445/create-networkx-graph-from-csv-file

edge_list = open('edge_count.csv', "r")
next(edge_list, None)  # get past the headers
GT = nx.Graph()

G = nx.parse_edgelist(edge_list, delimiter=',', create_using=GT,
                      nodetype=int, data=(('weight', int),))

print(G)

#G.edges.data()

# some network statistics as per lectures in Data Science Applications and Techniques, 
# David Weston, Birkbeck University, 2023
# Filtering the larger dataset down to the largest component
# Finding the largest component
connected_comps = [G.subgraph(s) for s in nx.connected_components(G)]
print('Sizes of connected components', [len(c) for c in connected_comps])
largest_component= connected_comps[0]
len(largest_component)

# creating a subgraph with only those nodes in the largest component
largest_graph = nx.subgraph(G, largest_component)
largest_graph.number_of_nodes()


# using cdlib to compare community detection algorithms
# cdlib - https://www.kaggle.com/code/bhavinmoriya/community-detection-algorithm 

#!pip install cdlib

import networkx as nx
from cdlib import algorithms

#pip install leidenalg

# Louvain algorithm
louvain_full = algorithms.louvain(G, weight='weight', resolution=1.)
louvain_largest_c = algorithms.louvain(largest_graph, weight='weight', resolution=1.)
print("Number of communities found by Louvain algorithm on full graph: ", len(louvain_full.communities))
print("Number of communities found by Louvain algorithm on largest component: ",len(louvain_largest_c.communities))
# Modularity
mod_louvain_full = louvain_full.newman_girvan_modularity()
mod_louvain_largest_c = louvain_largest_c.newman_girvan_modularity()
print("Modularity score for Louvain algorithm on full graph: ", mod_louvain_full.score)
print("Modularity score for Louvain algorithm on largest component: ", mod_louvain_largest_c.score)

# Leiden algorithm
leiden_full = algorithms.leiden(G, weights='weight')
leiden_largest_c = algorithms.leiden(largest_graph, weights='weight')
print("Number of communities found by Leiden algorithm on full graph: ",len(leiden_full.communities))
print("Number of communities found by Leiden algorithm on largest component: ",len(leiden_largest_c.communities))
# Modularity
mod_leiden_full = leiden_full.newman_girvan_modularity()
mod_leiden_largest_c = leiden_largest_c.newman_girvan_modularity()
print("Modularity score for Leiden algorithm on full graph: ", mod_leiden_full.score)
print("Modularity score for Leiden algorithm on largest component: ", mod_leiden_largest_c.score)


