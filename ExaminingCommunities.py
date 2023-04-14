# -*- coding: utf-8 -*-
"""
Created on Sat Apr  8 11:40:13 2023

Getting details of communities found by the Louvain Algorithm and looking at top 5 and then all 
members of each community in terms of degree centrality, and their associated locations

@author: Monique Brogan
"""

import networkx as nx
import csv
import community

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
                      nodetype=int, data=(('weight', int),))

print(G)

#G.edges.data()

# Filtering the larger dataset down to the largest component
# Connected components are sorted in descending order of their size - finding the largest component
connected_comps = [G.subgraph(s) for s in nx.connected_components(G)]
print('Sizes of the connected components', [len(c) for c in connected_comps])

largest_component= connected_comps[0]


# # list of degrees in largest component
# degree_list = largest_component.degree()
# print(degree_list)

# # list of nodes in largest component
# node_list = largest_component.nodes()
# print(node_list)

# # getting nodes with degree of greater than 1    
# higher_degrees = []
# for node in node_list:
#     print(node, degree_list[node])
#     if degree_list[node] > 1:
#         higher_degrees.append(node)

# print(higher_degrees)

# #largest_component_graph = nx.subgraph(G, largest_component)


# # creating a subgraph with only those nodes in the largest component, with degrees of more than 1
# HDG = nx.subgraph(G, higher_degrees)
# HDG.number_of_nodes()

largest_graph = nx.subgraph(G, largest_component)


#len(community_louvain.best_partition(HDG))

import community as community_louvain
import community

# compute the best partition
#partition = community_louvain.best_partition(HDG)
resolutions = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0]
for res in resolutions:
    partition = community_louvain.best_partition(largest_graph, weight='weight', resolution=res)
    print("Resolution value:", res, "# found communities smaller:", max(partition.values()))


partition = community_louvain.best_partition(largest_graph, weight='weight')
modularity = community.modularity(partition, largest_graph, weight='weight')
print("The modularity for the louvain algorithm when run on the largest component is", modularity)

print("# found communities smaller:", max(partition.values()))

#density = nx.density(HDG)
#print("Network density:", density)




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

print(communities_dict[0])

# getting the lengths for each comumunity to be able to sort them for the largest communities
community_lengths = {}
for key, value in communities_dict.items():
    print("key:", key, "length:", len(value))
    community_lengths[key] = len(value)

print(community_lengths)


# top 5 communities by number of members

top_5 = sorted(community_lengths.items(), key = lambda x: x[1], reverse = True)[:5]
print(top_5)

# getting top 5 members by degree centrality of top 5 communities, and checking locations
def top_five_communities(top_5_list, graph, communities_dictionary):
    for comm, count in top_5_list:
        location = [0,0,0,0]
        sub_community = nx.subgraph(graph, communities_dictionary[comm])
        degree = nx.degree_centrality(sub_community)
        highest_degree_centrality = sorted(degree.items(), key = lambda x: x[1], reverse = True)[:5]
        print('Degree centrality: ', highest_degree_centrality)
        for identifier, degree_c in highest_degree_centrality:
            print(comm, artists[str(identifier)], ", associated location", artists_communities[str(identifier)])
            location[artists_communities[str(identifier)]-1]+=1
        print(location)
        print("largest location as proportion of total size of community:", max(location)/5)
    

top_five_communities(top_5, largest_graph, communities_dict)



# getting all members by degree centrality of top 5 communities, and checking locations
def top_five_communities_all(top_5_list, graph, communities_dictionary):
    for comm, count in top_5_list:
        location = [0,0,0,0]
        sub_community = nx.subgraph(graph, communities_dictionary[comm])
        degree = nx.degree_centrality(sub_community)
        highest_degree_centrality = sorted(degree.items(), key = lambda x: x[1], reverse = True)
        print('Degree centrality: ', highest_degree_centrality)
        for identifier, degree_c in highest_degree_centrality:
            print(comm, artists[str(identifier)], ", associated location", artists_communities[str(identifier)])
            location[artists_communities[str(identifier)]-1]+=1
        print(location)
        print("largest location as proportion of total size of community:", max(location)/community_lengths[comm])
    

top_five_communities_all(top_5, largest_graph, communities_dict)


####################################################################################################
# top 5 communities by number of members
comms_sorted = sorted(community_lengths.items(), key = lambda x: x[1], reverse = True)
print(comms_sorted)
top_5 = sorted(community_lengths.items(), key = lambda x: x[1], reverse = True)[:5]
print(top_5)

# getting top 5 members by weighted degree of top 5 communities, and checking locations
def top_five_communities(top_5_list, graph, communities_dictionary):
    for comm, count in top_5_list:
        location = [0,0,0,0]
        sub_community = nx.subgraph(graph, communities_dictionary[comm])
        degree = list(sub_community.degree(weight = 'weight'))
        #print("DEGREE:", degree)
        srted = sorted(degree, key=lambda a: a[1], reverse=True)[:5]
        #print("SORTED DEGREES:", srted)
        #highest_degree_centrality = sorted(degree.items(), key = lambda x: x[1], reverse = True)[:5]
        #print('Degree centrality: ', highest_degree_centrality)
        for identifier, weighted_degree in srted:
            print(comm, artists[str(identifier)], ", associated location", artists_communities[str(identifier)])
            location[artists_communities[str(identifier)]-1]+=1
        print(location)
        print("largest location as proportion of total size of community:", max(location)/5)
    

top_five_communities(top_5, largest_graph, communities_dict)



# getting all members by degree centrality of top 5 communities, and checking locations
def top_five_communities_all(top_5_list, graph, communities_dictionary):
    for comm, count in top_5_list:
        location = [0,0,0,0]
        sub_community = nx.subgraph(graph, communities_dictionary[comm])
        degree = list(sub_community.degree(weight = 'weight'))
        srted = sorted(degree, key=lambda a: a[1], reverse=True)
        #print('Degree centrality: ', highest_degree_centrality)
        for identifier, weighted_degree in srted:
            print(comm, artists[str(identifier)], ", associated location", artists_communities[str(identifier)])
            location[artists_communities[str(identifier)]-1]+=1
        print(location)
        print("largest location as proportion of total size of community:", max(location)/community_lengths[comm])
    

top_five_communities_all(top_5, largest_graph, communities_dict)
