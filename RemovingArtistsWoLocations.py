# -*- coding: utf-8 -*-
"""
Removing artists from edge file and artist file that have no location (not able to be found)

@author: ##
"""
import pandas as pd

df_artists = pd.read_csv('artists_us_only_cleaned.csv', index_col= 0)

df_edges = pd.read_csv('edges_us_only_cleaned.csv', index_col= 0)

# those artists with no location found
df_artists_wo_locations = df_artists.loc[df_artists['Classification'].isna()]

# getting the user ids for artists without location
user_ids = df_artists_wo_locations['artistId']

# removing the artists without location artist ids from both columns in edge list
df_edges_col1_cleaned = df_edges[~df_edges["0"].isin(user_ids)]
df_edges_col2_cleaned = df_edges_col1_cleaned[~df_edges_col1_cleaned["1"].isin(user_ids)]

df_edges_col2_cleaned.to_csv('edges_with_locations.csv')

# creating an updated artist file with the new edges file to ensure we only have relevant artists
combined_nodes = pd.concat([df_edges_col2_cleaned['0'], df_edges_col2_cleaned['1']])

df_artists_w_locations = df_artists[df_artists["artistId"].isin(combined_nodes)]

# reset the index in the new dataframe
df_artists_w_locations.reset_index(drop=True, inplace=True)

df_artists_w_locations.to_csv('artists_with_classification_cleaned.csv')


