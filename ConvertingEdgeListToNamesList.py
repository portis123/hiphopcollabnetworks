# -*- coding: utf-8 -*-
"""
Created on Fri Mar 31 22:56:23 2023

@author: Monique Brogan

Creating an edge list with artist names instead of IDs from the original edge list from Discogs
"""
import pandas as pd
import csv
import numpy as np

# create a pandas dataframe from the edges file
df_edges = pd.read_csv('discogs_edges.csv')

# create a pandas dataframe from the artists file
df_artists = pd.read_csv('artists.csv')

# combine edge lists from both columns in edge list file
combined_nodes = pd.concat([df_edges['V1'], df_edges['V2']])

# sort node list in ascending order
combined_nodes = combined_nodes.sort_values()

# get unique values only
combined_nodes = combined_nodes.unique()

#len(combined_nodes)

np.savetxt("edge_list_combined.csv", combined_nodes, delimiter=",")

combined_list = pd.read_csv('edge_list_combined.csv')

#combined_list

combined_array = combined_list['artistIds'].to_numpy()

#len(combined_array)

df_artists_sorted = df_artists.sort_values(by=['artistId'])

#print(df_artists_sorted)

# Source: https://stackoverflow.com/questions/8078330/csv-writing-within-loop
def search_column_df(artist_df, edge_list):
    #list of row indexes that contain the search term
    with open('artist_id_names.csv','w', encoding="utf-8") as f1:
        writer=csv.writer(f1, delimiter=',',lineterminator='\n')
        writer.writerow(['artistId', 'artistName'])
        for i in edge_list:
            for row in artist_df.iterrows():
                #print("i", i)
                if i == row[1].values[0]:
                    print("row[1].values[0]", row[1].values[0])
                    #get row index
                    #row_index = row[0]
                    #add row index to dictionary
                    #rows.append([row[1].values[0], row[1].values[1]])
                    print([row[1].values[0], row[1].values[1]])
                    writer.writerow(([row[1].values[0], row[1].values[1]]))
                    break
    return

search_column_df(df_artists_sorted, combined_array)

df_artists_cleaned = pd.read_csv('artist_id_names.csv',encoding="latin1")
df_artists_cleaned

# create a dictionary of artist ids and names
map_dict = dict(zip(df_artists_cleaned.artistId,df_artists_cleaned.artistName))

# add columns with the names associated with the relevant artist ids in each column
df_edges['Names_lists1'] =  df_edges['V1'].explode().map(map_dict)
df_edges['Names_lists2'] =  df_edges['V2'].explode().map(map_dict)

# remove the artist ids and leave only the names
edge_list_names = df_edges.filter(['Names_lists1','Names_lists2'], axis=1)

#edge_list_names


edge_list_names.to_csv('df_edge_list_names.csv', index = False)






