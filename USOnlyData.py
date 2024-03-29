# -*- coding: utf-8 -*-
"""
@author: ##

Filtering dataset for artists based in the US only
"""
import pandas as pd
import numpy as np

# load file with artist ids, names and countries, as derived from MusicBrainz and other sources
df_locations = pd.read_excel('artist_id_names_country.xlsx')

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

# checking to make sure no anomalies
print(np.sort(df_locations_non_us['country'].unique().astype(str)))

# getting the artist ids from those not from the United States
artist_ids = df_locations_non_us['artistId']

df_edges = pd.read_csv('df_edges_cleaned.csv', index_col=0)

# removing V1 and V2 headers
df_edges = df_edges.iloc[1:]

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
df_artists_us_only = df_locations[df_locations["artistId"].isin(combined_nodes)]

# verify that only United States artists 
print(df_artists_us_only['country'].unique())

# reset the index in the new dataframe
df_artists_us_only.reset_index(drop=True, inplace=True)

df_artists_us_only.to_csv('artists_us_only.csv')

# as some data has been collected on artist city or region, get only those artists for which the info is missing
df_missing_location = df_artists_us_only[df_artists_us_only['location'].isna()]

df_missing_location.to_csv('artists_missing_locations.csv')