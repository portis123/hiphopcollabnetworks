# -*- coding: utf-8 -*-
"""
Created on Tue Mar  7 10:47:55 2023

@author: Monique Brogan

Filtering dataset for artists based in the US only
"""
import pandas as pd
import numpy as np


# load file with artist ids, names and countries, as derived from MusicBrainz
df_locations = pd.read_excel('artist_id_names_country.xlsx')
print(df_locations.head())
print(df_locations)

# Sense check that country column only contains countries and there are no different spellings of United States
countries = df_locations['country'].unique()
countries = countries.astype(str)
print(np.sort(countries))

# can see there are some with United States spelled as United states, verify this
print(df_locations[df_locations['country']== 'United states'])

# replace these with the correct version of United States
df_locations['country'] = df_locations['country'].replace('United states','United States')

# verify that this has worked
print(df_locations[df_locations['country']== 'United states'])


# those artists not from the US or with no location available
df_locations_non_us = df_locations.loc[df_locations["country"] !='United States']
print(df_locations_non_us.head())

# checking to make sure no anomalies
df_locations_non_us['country'].unique()


# getting the artist ids from those not from the United States
artist_ids = df_locations_non_us['artistId']
print(artist_ids)

df_edges = pd.read_csv('df_edges_cleaned.csv', index_col=0)
print(df_edges)

df_edges = df_edges.iloc[1:]
df_edges.head()

# checking data type to ensure columns are integers, like the artist ids
result = df_edges.dtypes
print(result)

# result returns object for both columns so need to convert them to integers

df_edges = df_edges.astype({"0":"int","1":"int"})

# removing the non-US artist ids from both columns in edge list
df_edges_col1_cleaned = df_edges[~df_edges['0'].isin(artist_ids)]
df_edges_col2_cleaned = df_edges_col1_cleaned[~df_edges_col1_cleaned['1'].isin(artist_ids)]

df_edges_col2_cleaned.to_csv('edges_us_only.csv')

# creating an updated artist file with the new edges file to ensure we only have artists with US location
combined_nodes = pd.concat([df_edges_col2_cleaned['0'], df_edges_col2_cleaned['1']])
#len(combined_nodes.unique())

df_artists_us_only = df_locations[df_locations["artistId"].isin(combined_nodes)]
print(df_artists_us_only)

# remove the duplicates from the artist list we have just created 
df_artists_us_unique = df_artists_us_only[~df_artists_us_only['artistName'].str.lower().duplicated()]
print(df_artists_us_unique)

# verify that only United States artists 
print(df_artists_us_unique['country'].unique())

# reset the index in the new dataframe
df_artists_us_unique.reset_index(drop=True, inplace=True)

print(df_artists_us_unique.head())

df_artists_us_unique.to_csv('artists_us_only.csv')


# as some data has been collected on artist city or region, get only those artists for which the info is missing
df_missing_location = df_artists_us_unique[df_artists_us_unique['location'].isna()]

print(df_missing_location.head())

df_missing_location.to_csv('artists_missing_locations.csv')