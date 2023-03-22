# -*- coding: utf-8 -*-
"""
Created on Wed Mar 22 14:03:34 2023

@author: moniq
Counting the number of edges between the same two artists. The original intent of this was 
to look at edge weights and how these would work. This exercise showed, when checking some 
of the most common pairings, that artists were often shown as collaborating or appearing on 
the same master release as one of their aliases - as verified by checking the two involved 
artist IDs (see 'Extracting Artist Aliases and Removing Collaborations between Artists and 
            Themselves')
"""
import pandas as pd

# edge list derived from discogs dataset
df_edges = pd.read_csv('discogs_edges.csv')

#df_edges.head()

# count the number of times the same nodes have collaborated
df_edge_count = df_edges.groupby(["V1", "V2"]).size().reset_index(name="No times collaborated").sort_values('No times collaborated', ascending=False)

df_edge_count.head()

df_edge_count.to_csv('edge_count.csv', index = False)

# number of pairs of nodes for each number of collaborations 
df_edge_count['No times collaborated'].value_counts()

