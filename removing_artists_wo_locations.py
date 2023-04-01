# -*- coding: utf-8 -*-
"""
Created on Sun Mar 19 18:33:54 2023

@author: Monique Brogan
"""
import pandas as pd

df_artists = pd.read_csv('artists_us_only_cleaned.csv', index_col= 0)
print(df_artists)

df_edges = pd.read_csv('edges_us_only_cleaned.csv', index_col= 0)
print(df_edges)

# those artists with no location found
df_artists_wo_locations = df_artists.loc[df_artists['Classification'].isna()]
#print(df_artists_wo_locations['Classification'])

# getting the user ids for artists without location
user_ids = df_artists_wo_locations['artistId']
print(user_ids)

# removing the artists without location artist ids from both columns in edge list
df_edges_col1_cleaned = df_edges[~df_edges["0"].isin(user_ids)]
df_edges_col2_cleaned = df_edges_col1_cleaned[~df_edges_col1_cleaned["1"].isin(user_ids)]
print(df_edges_col2_cleaned)

df_edges_col2_cleaned.to_csv('edges_with_locations.csv')


# creating an updated artist file with the new edges file to ensure we only have relevant artists
combined_nodes = pd.concat([df_edges_col2_cleaned['0'], df_edges_col2_cleaned['1']])
#len(combined_nodes.unique())


df_artists_w_locations = df_artists[df_artists["artistId"].isin(combined_nodes)]
print(df_artists_w_locations.head())

# remove the duplicates from the artist list we have just created, if any
#df_artists_w_locations_unique =df_artists_w_locations[~df_artists_w_locations['artistName'].str.lower().duplicated()]
#print(df_artists_w_locations_unique)


# reset the index in the new dataframe
df_artists_w_locations.reset_index(drop=True, inplace=True)

print(df_artists_w_locations)

df_artists_w_locations.to_csv('artists_with_classification_cleaned.csv')


