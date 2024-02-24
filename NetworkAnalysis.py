# -*- coding: utf-8 -*-
"""
Running network analytics on the US hip hop artists dataset

@author: ##
"""
import networkx as nx
import csv

# some network statistics queries adapted from lectures in Data Science Applications and Techniques, David Weston, Birkbeck 
# University, 2023

# create dictionary of artist ids with names - removed header from artists_with_location_codes_simpler.csv 
# file and saved it as artists_with_location_codes_simpler_for_dict.csv
artists = {}
with open('artists_with_location_codes_simpler_for_dict.csv', 'r', encoding="utf8") as file:
    reader = csv.reader(file)
    for row in reader:
        artist_id = row[1]
        artist_name = row[2]
        artists[artist_id] = artist_name
        

# import edge file with weight details included
# https://stackoverflow.com/questions/49683445/create-networkx-graph-from-csv-file

edge_list = open('edge_count.csv', "r")
next(edge_list, None)  # get past the headers
GT = nx.Graph()

G = nx.parse_edgelist(edge_list, delimiter=',', create_using=GT,
                      nodetype=int, data=(('weight', int),))


# get information on number of nodes, number of edges
discogs_n, discogs_e = G.order(), G.size()
print('Nodes: ', discogs_n)
print('Edges: ', discogs_e)

# calculate weighted degree correlation coefficient for full graph
r = nx.degree_pearson_correlation_coefficient(G, weight='weight')
print(r)

# creating ground truth basis - artists with their locations as per my research
artists_communities = {}
with open('artists_with_location_codes_simpler_for_dict.csv', 'r', encoding="utf8") as file:
    reader = csv.reader(file)
    for row in reader:
        artist_id = row[1]
        location_code = int(row[6])
        artists_communities[artist_id] = location_code

# artist location classifier
def classifyArtistLocation(code):
    location = "Not classified"
    if code == 1:
        location = "East Coast"
    elif code == 2:
        location = "Midwest"
    elif code == 3:
        location = "Southern"
    elif code == 4:
        location = "West Coast"
    return location


def top_10_between(graph):
    betweenness_discogs = nx.betweenness_centrality(graph, weight='weight')
    top_10 = sorted(betweenness_discogs.items(), key = lambda x: x[1], reverse = True)[:10]
    print('Discogs betweenness centrality (top 10):', top_10)
    for identifier, betw_c in top_10:
        print(identifier, artists[str(identifier)], ", associated location:", classifyArtistLocation(artists_communities[str(identifier)]))
        
# top 10 artists in terms of betweenness centrality for full network
top_10_between(G)   


# get information on connected components and find largest connected component
connected_comps = [G.subgraph(s) for s in nx.connected_components(G)]
print('Sizes of connected components', [len(c) for c in connected_comps])
largest_component= connected_comps[0]

# create subgraph of largest component
largest_graph = nx.subgraph(G, largest_component)

# top 10 artists in terms of betweenness centrality for largest component
top_10_between(largest_graph)   


# get information on number of nodes, number of edges for largest component graph
discogs_largest_n, discogs_largest_e = largest_graph.order(), largest_graph.size()
print('Nodes: ', discogs_largest_n)
print('Edges: ', discogs_largest_e)

# calculate degree correlation coefficient for subgraph
r = nx.degree_pearson_correlation_coefficient(largest_graph, weight='weight')
print(r)






