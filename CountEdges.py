# -*- coding: utf-8 -*-
"""
Created on Wed Mar 22 14:03:34 2023

Counting the number of edges between the same two artists. Getting edge weights for frequent collaborations

@author: Monique Brogan
"""
import pandas as pd

# edge list derived from discogs dataset
df_edges = pd.read_csv('edges_w_locations_removed_multiple.csv', index_col=0)

df_edges.head()

# count the number of times the same nodes have collaborated
df_edge_count = df_edges.groupby(["0", "1"]).size().reset_index(name="Weight").sort_values('Weight', ascending=False)

df_edge_count

df_edge_count.to_csv('edge_count.csv', index = False)

# number of pairs of nodes for each number of collaborations 
df_edge_count['No times collaborated'].value_counts()

