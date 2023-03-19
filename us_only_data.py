# -*- coding: utf-8 -*-
"""
Created on Tue Mar  7 10:47:55 2023

@author: moniq
"""
import pandas as pd

df_locations = pd.read_excel('artists_cleaned_after_duplicates.xlsx')
print(df_locations.head())
print(df_locations)

print(df_locations['country'].unique())

# those artists not from the US or with no location available
df_locations_non_us = df_locations.loc[df_locations["country"] !='United States']
print(df_locations_non_us.head())

user_ids = df_locations_non_us['artistId']
#print(user_ids)

df_edges = pd.read_csv('df_edges_cleaned.csv')
#print(df_edges)

# removing the non-US artist ids from both columns in edge list
df_edges_v1_cleaned = df_edges[~df_edges["V1"].isin(user_ids)]
df_edges_v2_cleaned = df_edges_v1_cleaned[~df_edges_v1_cleaned["V2"].isin(user_ids)]

df_edges_v2_cleaned.to_csv('edges_us_only.csv')

# creating an updated artist file with the new edges file to ensure we only have artists with US location
combined_nodes = pd.concat([df_edges_v2_cleaned['V1'], df_edges_v2_cleaned['V2']])

df_artists_us_only = df_locations[df_locations["artistId"].isin(combined_nodes)]
print(df_artists_us_only)

# remove the duplicates from the artist list we have just created
df_artists_us_unique = df_artists_us_only[~df_artists_us_only['artistName'].str.lower().duplicated()]
print(df_artists_us_unique)

print(df_artists_us_unique['country'].unique())



# reset the index in the new dataframe
df_artists_us_unique.reset_index(drop=True, inplace=True)

print(df_artists_us_unique.head())

#df_artists_us_unique.to_csv('artists_us_only.csv')

df_missing_location = df_artists_us_unique[df_artists_us_unique['location'].isna()]

print(df_missing_location.head())

df_missing_location.to_csv('artists_missing_locations.csv')