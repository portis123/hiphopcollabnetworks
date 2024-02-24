# -*- coding: utf-8 -*-
"""
Counting the number of edges between the same two artists. Getting edge weights for frequent collaborations

@author: ##
"""
import pandas as pd

# edge list derived from discogs dataset
df_edges = pd.read_csv('edges_w_locations_removed_multiple.csv', index_col=0)

# count the number of times the same nodes have collaborated
df_edge_count = df_edges.groupby(["0", "1"]).size().reset_index(name="weight").sort_values('weight', ascending=False)

# number of pairs of nodes for each number of collaborations / weight
df_edge_count['weight'].value_counts()

df_edge_count.to_csv('edge_count.csv', index = False)



