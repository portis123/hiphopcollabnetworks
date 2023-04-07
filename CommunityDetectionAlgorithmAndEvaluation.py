# -*- coding: utf-8 -*-
"""
Created on Sun Apr  2 14:41:31 2023

Creating a ground truth to compare results against, running the Louvain algorithm over full dataset, 
including nodes and graph files, and evaluating results

@author: Monique Brogan
"""

import networkx as nx
import csv
import community
import numpy as np


# creating ground truth basis
artists_communities = {}
with open('artists_with_location_codes_simpler_for_dict.csv', 'r', encoding="utf8") as file:
    reader = csv.reader(file)
    for row in reader:
        artist_id = row[1]
        #artist_name = row[2]
        location_code = int(row[6])
        artists_communities[artist_id] = location_code
        
print(artists_communities)

# Source: https://programminghistorian.org/en/lessons/exploring-and-analyzing-network-data-with-python

# getting nodes for graph
with open(r'C:\Users\moniq\Documents\Repositories\bsc-project-22_23---source-code-portis123\artists_with_location_codes_simpler.csv', 'r') as nodefile: 
   reader = csv.reader(nodefile)
    # Getting the data without the header
   nodes = [n for n in reader][1:]

node_ids = [n[1] for n in nodes] # List of node ids


# getting edges for graph        
with open('edges_w_locations_removed_multiple_no_index.csv', 'r') as edgefile: 
    reader = csv.reader(edgefile) 
    edges = [tuple(e) for e in reader][1:] 
    
G = nx.Graph()
G.add_nodes_from(node_ids)
G.add_edges_from(edges)
partition = community.best_partition(G)
print(partition)


# https://scikit-learn.org/stable/modules/classes.html#module-sklearn.metrics
from sklearn.metrics import confusion_matrix, precision_score, recall_score, f1_score, precision_recall_fscore_support

ground_truth = [artists_communities[node] for node in G.nodes()]
predicted = [partition[node] for node in G.nodes()]

c_matrix = confusion_matrix(ground_truth, predicted)
#print(c_matrix)

prec_score = precision_score(ground_truth, predicted, average = 'weighted')
print(prec_score)
rec_score = recall_score(ground_truth, predicted, average = 'weighted')
print(rec_score)
f1 = f1_score(ground_truth, predicted, average='weighted')
print(f1)

print(precision_recall_fscore_support(ground_truth, predicted, average='weighted'))
