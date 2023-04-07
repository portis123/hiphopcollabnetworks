# -*- coding: utf-8 -*-
"""
Created on Sun Apr  2 18:22:04 2023

Running network analytics on the Discogs dataset

@author: Monique Brogan
"""
import numpy as np
import networkx as nx
import csv
import pandas as pd
from networkx.algorithms import community

import matplotlib.pylab as plt

# matplotlib specifications and some network statistics as per lectures in Data Science Applications 
# and Techniques, David Weston, Birkbeck University, 2023
%matplotlib inline 
plt.style.use('seaborn-white')
plt.rc('text', usetex = False)
plt.rc('xtick', labelsize = 10) 
plt.rc('ytick', labelsize = 10) 
plt.rc('font', size = 12) 
plt.rc('figure', figsize = (12, 5))

# create dictionary of artist ids with names
artists = {}
with open('artists_with_location_codes_simpler_for_dict.csv', 'r', encoding="utf8") as file:
    reader = csv.reader(file)
    for row in reader:
        artist_id = row[1]
        artist_name = row[2]
        artists[artist_id] = artist_name
        
print(artists)

# import edge file
# https://stackoverflow.com/questions/49683445/create-networkx-graph-from-csv-file

edge_list = open('edge_count.csv', "r")
next(edge_list, None)  # get past the headers
GT = nx.Graph()

G = nx.parse_edgelist(edge_list, delimiter=',', create_using=GT,
                      nodetype=int, data=(('Weight', int),))

print(G)

#G.edges.data()


# get information on number of nodes, number of edges and average degree
discogs_n, discogs_k = G.order(), G.size()
discogs_avg_deg = discogs_k / discogs_n
print('Nodes: ', discogs_n)
print('Edges: ', discogs_k)
print('Average degree: ', discogs_avg_deg)

# get the degree distribution
degrees =  [d for n,d in G.degree()] #extract all the degrees for each node
degree_hist = plt.hist(degrees, 100)
plt.xlabel('Degree')
plt.ylabel('Number of nodes')
plt.title('Degree distribution')
plt.savefig("./degree_hist_plt.png", dpi = 300, bbox_inches = 'tight')

# get information on connected components
print('Number of connected components of Discogs US hip hop network: ', nx.number_connected_components(G))
discogs_components = nx.connected_components(G)
print('Sizes of the connected components', [len(c) for c in discogs_components])

# calculate degree correlation coefficient
r = nx.degree_pearson_correlation_coefficient(G)

print(f"{r:3.1f}")

# top 10 artists in terms of betweenness centrality
betweenness_discogs = nx.betweenness_centrality(G)
top_10 = sorted(betweenness_discogs.items(), key = lambda x: x[1], reverse = True)[:10]
print(top_10)
print('Discogs betweenness centrality:', sorted(betweenness_discogs.items(), key = lambda x: x[1], reverse = True)[:10])
for identifier, betw_c in top_10:
    print(identifier, artists[str(identifier)])
    
    
# network transitivity score
print(nx.transitivity(G))

# Connected components are sorted in descending order of their size - getting largest component
connected_comps = [G.subgraph(s) for s in nx.connected_components(G)]
largest_component= connected_comps[0]
largest_component

between_cen= nx.betweenness_centrality(largest_component)
print(between_cen)
top_10 = sorted(between_cen.items(), key = lambda x: x[1], reverse = True)[:10]
for identifier, betw_c in top_10:
    print(identifier, artists[str(identifier)])

# getting the nodes in the largest component which have a degree of 
# more than 1
degree_list = largest_component.degree()

node_list = largest_component.nodes()
print(node_list)
    
higher_degrees = []
for node in node_list:
    print(node, degree_list[node])
    if degree_list[node] > 1:
        higher_degrees.append(node)

# filtering down graph to largest component with more than one degree
HDG = nx.subgraph(G, higher_degrees)

# Stats for filtered graph

# top 10 artists in terms of betweenness centrality
between_cen_hd= nx.betweenness_centrality(HDG)
print(between_cen_hd)
top_10 = sorted(between_cen_hd.items(), key = lambda x: x[1], reverse = True)[:10]
print(top_10)
for identifier, betw_c in top_10:
    print(identifier, artists[str(identifier)])

# get information on number of nodes, number of edges and average degree
discogs_largest_n, discogs_largest_k = HDG.order(), HDG.size()
discogs_avg_deg_largest = discogs_largest_k / discogs_largest_n
print('Nodes: ', discogs_largest_n)
print('Edges: ', discogs_largest_k)
print('Average degree: ', discogs_avg_deg_largest)

# calculate degree correlation coefficient for subgraph
r = nx.degree_pearson_correlation_coefficient(HDG)

print(f"{r:3.1f}")

# refined network transitivity score
print(nx.transitivity(HDG))


# finding communities #1
import community

partition = community.best_partition(HDG)

print("# found communities:", max(partition.values()))


# finding communities #2
import networkx as nx
import numpy as np
from community import community_louvain
comms = community_louvain.best_partition(HDG)
print("# found communities:", max(comms.values()))

# finding communities #3
import community
partition = community.best_partition(HDG)
modularity = community.modularity(partition, HDG)

pos = nx.spring_layout(HDG, dim=2)

community_id = [partition[node] for node in HDG.nodes()]

fig = plt.figure(figsize=(10, 10))
nx.draw(
        HDG,
        pos,
        edge_color=['silver'] * len(HDG.edges()),
        cmap=plt.cm.tab20,
        node_color=community_id,
        node_size=150,
        )

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

# evaluating results

# https://scikit-learn.org/stable/modules/classes.html#module-sklearn.metrics

from sklearn.metrics import confusion_matrix, precision_score, recall_score, f1_score, precision_recall_fscore_support

ground_truth = [artists_communities[str(node)] for node in HDG.nodes()]
predicted = [partition[node] for node in HDG.nodes()]

c_matrix = confusion_matrix(ground_truth, predicted)
#print(c_matrix)

prec_score = precision_score(ground_truth, predicted, average = 'weighted')
print(prec_score)
rec_score = recall_score(ground_truth, predicted, average = 'weighted')
print(rec_score)
f1 = f1_score(ground_truth, predicted, average='weighted')
print(f1)

print(precision_recall_fscore_support(ground_truth, predicted, average='weighted'))

