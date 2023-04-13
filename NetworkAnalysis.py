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

# create dictionary of artist ids with names - removed header from artists_with_location_codes_simpler.csv 
# file and saved it as artists_with_location_codes_simpler_for_dict.csv
artists = {}
with open('artists_with_location_codes_simpler_for_dict.csv', 'r', encoding="utf8") as file:
    reader = csv.reader(file)
    for row in reader:
        artist_id = row[1]
        artist_name = row[2]
        artists[artist_id] = artist_name
        
print(artists)

# import edge file with weight details included
# https://stackoverflow.com/questions/49683445/create-networkx-graph-from-csv-file

edge_list = open('edge_count.csv', "r")
next(edge_list, None)  # get past the headers
GT = nx.Graph()

G = nx.parse_edgelist(edge_list, delimiter=',', create_using=GT,
                      nodetype=int, data=(('Weight', int),))

print(G)

# G.edges.data()

# edge_weights =[]
# for edge1, edge2, weight in G.edges.data():
#     edge_weights.append(weight)
# print(edge_weights)


# get information on number of nodes, number of edges
discogs_n, discogs_e = G.order(), G.size()
print('Nodes: ', discogs_n)
print('Edges: ', discogs_e)

# calculate weighted degree correlation coefficient for full graph
r = nx.degree_pearson_correlation_coefficient(G, weight='Weight')

print(r)

# top 10 artists in terms of betweenness centrality for full network
betweenness_discogs = nx.betweenness_centrality(G, weight='Weight')
top_10 = sorted(betweenness_discogs.items(), key = lambda x: x[1], reverse = True)[:10]
print('Discogs betweenness centrality (top 10):', top_10)
for identifier, betw_c in top_10:
    print(identifier, artists[str(identifier)])
    
    
# get information on connected components and find largest connected component
connected_comps = [G.subgraph(s) for s in nx.connected_components(G)]
print('Sizes of connected components', [len(c) for c in connected_comps])
largest_component= connected_comps[0]
len(largest_component)

largest_graph = nx.subgraph(G, largest_component)

# top 10 artists in terms of betweenness centrality for largest component
between_cen_hd= nx.betweenness_centrality(largest_graph, weight='Weight')
#print(between_cen_hd)
top_10 = sorted(between_cen_hd.items(), key = lambda x: x[1], reverse = True)[:10]
print('Discogs betweenness centrality (top 10) for largest component:', top_10)
for identifier, betw_c in top_10:
    print(identifier, artists[str(identifier)])

# get information on number of nodes, number of edges
discogs_largest_n, discogs_largest_e = largest_graph.order(), largest_graph.size()
print('Nodes: ', discogs_largest_n)
print('Edges: ', discogs_largest_e)

# calculate degree correlation coefficient for subgraph
r = nx.degree_pearson_correlation_coefficient(largest_graph, weight='Weight')

print(r)






