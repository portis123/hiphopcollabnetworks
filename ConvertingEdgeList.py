# -*- coding: utf-8 -*-
"""
Creating an edge list with artist names instead of IDs from the original edge list from Discogs.
Also filtering down larger artist id and names list from Discogs masters file to only include those
in our analysis

@author: Monique Brogan
"""

import pandas as pd

# create a pandas dataframe from the edges file
df_edges = pd.read_csv('discogs_edges.csv')

# create a pandas dataframe from the artists file
df_artists = pd.read_csv('artists.csv')

# combine edge lists from both columns in edge list file
combined_nodes = pd.concat([df_edges['V1'], df_edges['V2']])
combined_nodes

# get only the artists that are in the list of nodes from our edge list
df_artists_hh_new = df_artists[df_artists["artistId"].isin(combined_nodes)]

# remove the duplicates from the artist list we have just created
df_artists_cleaned = df_artists_hh_new[~df_artists_hh_new['artistName'].str.lower().duplicated()]
print(df_artists_cleaned)

# reset the index in the new dataframe
df_artists_cleaned.reset_index(drop=True, inplace=True)

df_artists_cleaned

df_artists_sorted = df_artists_cleaned.sort_values(by=['artistId'])
df_artists_sorted.reset_index(drop=True, inplace=True)
df_artists_sorted

# save list of relevant artist ids and names
df_artists_sorted.to_csv('df_artists_cleaned.csv')

# create a dictionary of artist ids and names
map_dict = dict(zip(df_artists_cleaned.artistId,df_artists_cleaned.artistName))
# add columns with the names associated with the relevant artist ids in each column
df_edges['Names_lists1'] =  df_edges['V1'].explode().map(map_dict)
df_edges['Names_lists2'] =  df_edges['V2'].explode().map(map_dict)

#df_edges.head()

# remove the artist ids and leave only the names
edge_list_names = df_edges.filter(['Names_lists1','Names_lists2'], axis=1)

edge_list_names.head()

# save edge list of artist names
edge_list_names.to_csv('df_edge_list_names.csv')