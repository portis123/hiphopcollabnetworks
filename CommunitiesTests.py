# -*- coding: utf-8 -*-
"""
Created on Thu Apr  6 11:16:38 2023

Running Louvain, Leiden and Walktrap algorithms and comparing
modularity scores

@author: Monique Brogan
"""

import numpy as np
import networkx as nx
import csv
import pandas as pd
import matplotlib.pylab as plt


# matplotlib specifications as per lectures in Data Science Applications and Techniques, 
# David Weston, Birkbeck University, 2023
%matplotlib inline 
plt.style.use('seaborn-white')
plt.rc('text', usetex = False)
plt.rc('xtick', labelsize = 10) 
plt.rc('ytick', labelsize = 10) 
plt.rc('font', size = 12) 
plt.rc('figure', figsize = (12, 5))


# import edge file
# https://stackoverflow.com/questions/49683445/create-networkx-graph-from-csv-file

edge_list = open('edge_count.csv', "r")
next(edge_list, None)  # get past the headers
GT = nx.Graph()

G = nx.parse_edgelist(edge_list, delimiter=',', create_using=GT,
                      nodetype=int, data=(('Weight', int),))

print(G)

#G.edges.data()

# Filtering the larger dataset down to the largest component
# Connected components are sorted in descending order of their size - finding the largest component
connected_comps = [G.subgraph(s) for s in nx.connected_components(G)]
largest_component= connected_comps[0]
largest_component

# list of degrees in largest component
degree_list = largest_component.degree()
print(degree_list)

# list of nodes in largest component
node_list = largest_component.nodes()
print(node_list)

# getting nodes with degree of greater than 1    
higher_degrees = []
for node in node_list:
    print(node, degree_list[node])
    if degree_list[node] > 1:
        higher_degrees.append(node)

print(higher_degrees)

#largest_component_graph = nx.subgraph(G, largest_component)


# creating a subgraph with only those nodes in the largest component, with degrees of more than 1
HDG = nx.subgraph(G, higher_degrees)
HDG.number_of_nodes()



# using cdlib to compare community detection algorithms
# cdlib - https://www.kaggle.com/code/bhavinmoriya/community-detection-algorithm 

#!pip install cdlib

import networkx as nx
from cdlib import algorithms, evaluation

#pip install leidenalg

import igraph
import leidenalg

# Louvain algorithm
louvain = algorithms.louvain(test_graph_g, weight='weight', resolution=1., randomize=False)
print(len(louvain.communities))
# Modularity
mod_louvain = louvain.newman_girvan_modularity()
mod_louvain

# Leiden algorithm
leiden = algorithms.leiden(HDG)
print(len(leiden.communities))
# Modularity
mod_leiden = leiden.newman_girvan_modularity()
print(mod_leiden)

# Walktrap algorithm
walktrap = algorithms.walktrap(HDG)
print(len(walktrap.communities))
# Modularity
mod_walktrap = walktrap.newman_girvan_modularity()
print(mod_walktrap)

# Plotting the modularity scores
algorithms = ['Louvain', 'Leiden', 'Walktrap']
evaluation = [mod_louvain.score, mod_leiden.score, mod_walktrap.score]
df_modularity = pd.DataFrame({"Algorithms":algorithms,
                              "Modularity Score":evaluation})
	
modularity_sorted= df_modularity.sort_values('Modularity Score')
plt.bar('Algorithms', 'Modularity Score',data=modularity_sorted, color=['darkseagreen', 'mediumaquamarine', 'cornflowerblue'])
plt.ylabel('Modularity')
plt.title('Comparison of performance of Community Detection Algorithms')
plt.show()

