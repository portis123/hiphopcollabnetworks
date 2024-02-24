# -*- coding: utf-8 -*-
"""
Getting details of communities found by the Louvain Algorithm and looking at all communities returned and then top 5 by size for 
location trends. Also looking at top 5 artists by weighted degree in each of the 5 largest communities and their location trends

@author: ##
"""

import networkx as nx
import csv
import community as community_louvain

# creating ground truth basis - dictionary of artist ids along with their assigned communities (as per the locations found 
# in my research)
artists_communities = {}
with open('artists_with_location_codes_simpler_for_dict.csv', 'r', encoding="utf8") as file:
    reader = csv.reader(file)
    for row in reader:
        artist_id = row[1]
        location_code = int(row[6])
        artists_communities[artist_id] = location_code

# create dictionary of artist ids with names
artists = {}
with open('artists_with_location_codes_simpler_for_dict.csv', 'r', encoding="utf8") as file:
    reader = csv.reader(file)
    for row in reader:
        artist_id = row[1]
        artist_name = row[2]
        artists[artist_id] = artist_name

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

# import edge file
# https://stackoverflow.com/questions/49683445/create-networkx-graph-from-csv-file

edge_list = open('edge_count.csv', "r")
next(edge_list, None)  # get past the headers
GT = nx.Graph()

G = nx.parse_edgelist(edge_list, delimiter=',', create_using=GT,
                      nodetype=int, data=(('weight', int),))


# looking at communities for full network
partition_full = community_louvain.best_partition(G, weight='weight')
modularity_full = community_louvain.modularity(partition_full, G, weight='weight')
print("The modularity for the louvain algorithm when run on the whole network is", modularity_full)

print("# found communities:", max(partition_full.values()))

# Filtering the larger network down to the largest component
connected_comps = [G.subgraph(s) for s in nx.connected_components(G)]
print('Sizes of the connected components', [len(c) for c in connected_comps])

largest_component= connected_comps[0]

# creating a subgraph from the largest component
largest_graph = nx.subgraph(G, largest_component)


# does changing resolution value bring community size closer to ground truth (resolution is 1.0 by default)
resolutions = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0]
for res in resolutions:
    partition = community_louvain.best_partition(largest_graph, weight='weight', resolution=res)
    print("Resolution value:", res, "# found communities smaller:", max(partition.values()))

# using a resolution value other than the default of 1.0 doesn't bring the number of communities any closer so will use default
 
# running the louvain algorithm on the largest component
partition = community_louvain.best_partition(largest_graph, weight='weight')
modularity = community_louvain.modularity(partition, largest_graph, weight='weight')
print("The modularity for the louvain algorithm when run on the largest component is", modularity)

print("# found communities:", max(partition.values()))


# counting number of artists in each community
import collections
community_count = collections.Counter(partition.values())
print(community_count)

# creating a dictionary with each community and its artist ids
num_communities = len(community_count)
communities_dict = {}
for i in range(0, num_communities):
    communities_dict[i] = []
    
for key, value in partition.items():
    communities_dict.setdefault(value).extend([key])


# getting the lengths for each community to be able to sort them for the largest communities
community_lengths = {}
for key, value in communities_dict.items():
    print("Community Number:", key, ", Size:", len(value))
    community_lengths[key] = len(value)

# communities sorted by number of members
comms_sorted = sorted(community_lengths.items(), key = lambda x: x[1], reverse = True)

# 5 largest communities
top_5 = sorted(community_lengths.items(), key = lambda x: x[1], reverse = True)[:5]

# looking at community members, their associated locations and tallying which artists are associated with which locations, then 
# counting location in community with highest number of members
def all_members(comms_list, graph, communities_dictionary):
    for comm, count in comms_list:
        # list for locations - to be used as counter, index 0 for East Coast, index 1 for Midwest, index 2 for Southern, index 3 for West Coast
        location = [0,0,0,0]
        # make a subgraph of the community
        sub_community = nx.subgraph(graph, communities_dictionary[comm])
        # get a list of weighted degrees for the community
        degree = list(sub_community.degree(weight = 'weight'))
        # sort the weighted degrees
        srted = sorted(degree, key=lambda a: a[1], reverse=True)
        for identifier, weighted_degree in srted:
            print(comm, artists[str(identifier)], ", associated location:", classifyArtistLocation(artists_communities[str(identifier)]))
            # incrementing relevant index with location code, 0 index is for 1 (East Coast), 1 index is for 2 (Midwest) etc
            location[artists_communities[str(identifier)]-1]+=1
        print("community:", comm) 
        print(location)
        print("largest location as proportion of total size of community:", max(location)/count)
    
# looking at all communities
all_members(comms_sorted, largest_graph, communities_dict)
# looking at top 5 communities
all_members(top_5, largest_graph, communities_dict)

# getting top 5 members by weighted degree of top 5 communities, and checking locations
def top_five_members(top_5_list, graph, communities_dictionary):
    for comm, count in top_5_list:
        # list for locations - to be used as counter, index 0 for East Coast, index 1 for Midwest, index 2 for Southern, index 3 for West Coast
        location = [0,0,0,0]
        # make a subgraph of the community
        sub_community = nx.subgraph(graph, communities_dictionary[comm])
        # get a list of weighted degrees for the community
        degree = list(sub_community.degree(weight = 'weight'))
        # sort the weighted degrees and get top 5 by weighted degree
        srted = sorted(degree, key=lambda a: a[1], reverse=True)[:5]
        for identifier, weighted_degree in srted:
            print(comm, artists[str(identifier)], ", associated location:", classifyArtistLocation(artists_communities[str(identifier)]))
            # incrementing relevant index with location code, 0 index is 1 (East Coast), 1 index is 2 (Midwest) etc
            location[artists_communities[str(identifier)]-1]+=1
        print(location)
        print("largest location as proportion of total size of community:", max(location)/5)
    

top_five_members(top_5, largest_graph, communities_dict)
