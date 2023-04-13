# -*- coding: utf-8 -*-
"""
Created on Sun Mar 19 16:27:57 2023

Removing artists that have been marked to remove because of being labels rather than artists, having incorrect 
country data (not US - found when adding locations) or not being musicians but rather actors (Saget) or other non-musicians (Malcolm X)

@author: Monique Brogan
"""
import pandas as pd

df_artists = pd.read_excel('artists_us_only_w_location.xlsx', index_col= 0)
print(df_artists)

# those artists tagged with remove
df_artists_to_remove = df_artists.loc[df_artists["Alias"] == "REMOVE"]
print(df_artists_to_remove)

user_ids = df_artists_to_remove['artistId']
print(user_ids)

df_edges = pd.read_csv('edges_us_only.csv', index_col= 0)
print(df_edges)

# removing the artists to be removed artist ids from both columns in edge list
df_edges_col1_cleaned = df_edges[~df_edges["0"].isin(user_ids)]
df_edges_col2_cleaned = df_edges_col1_cleaned[~df_edges_col1_cleaned["1"].isin(user_ids)]

df_edges_col2_cleaned.to_csv('edges_us_only_cleaned.csv')

# creating an updated artist file with the new edges file to ensure we only have relevant artists
combined_nodes = pd.concat([df_edges_col2_cleaned['0'], df_edges_col2_cleaned['1']])
len(combined_nodes.unique())

df_artists_cleaned = df_artists[df_artists["artistId"].isin(combined_nodes)]
len(df_artists_cleaned)

# reset the index in the new dataframe
df_artists_cleaned.reset_index(drop=True, inplace=True)

print(df_artists_cleaned.head)

df_artists_cleaned.to_csv('artists_us_only_cleaned.csv')

