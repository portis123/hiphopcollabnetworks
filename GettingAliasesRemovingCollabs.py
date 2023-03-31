# -*- coding: utf-8 -*-
"""
Created on Wed Mar 22 14:16:01 2023

@author: Monique Brogan
"""

# Used the xmltodict library to get details of artists' aliases in a dataframe alongside their 
# artist ids and names. 
# Source: https://python.plainenglish.io/saving-xml-content-to-a-pandas-dataframe-using-xmltodict-b6fab32a5100. 
# Then removed all instances from the edge list where an artist is shown as collaborating 
# with themselves.

#pip install xmltodict

# to help with decompressing Discogs data dump file
import gzip

import xmltodict
import pandas as pd
import csv

# import list of artist ids and artist names
df_cleaned = pd.read_csv('artist_id_names.csv', encoding="latin1")


df_cleaned

# parsing the Discogs artists file 
artists_file = xmltodict.parse(gzip.GzipFile('discogs_20180901_artists.xml.gz'))

# refining the data to look at the artists
artists_file = artists_file['artists']['artist']

# first value in artists dataset
artists_file[0]

# function to get an artist's id, name and alias, and put these in a dataframe
def get_artist_data(artist):
    data= []
    artist_id = artist["id"]
    artist_name = artist["name"]
    try:
        aliases = artist['aliases']['name']
    except:
        aliases = "none available"
    data.append({"id": artist_id, "name": artist_name, "aliases": aliases})
    df = pd.DataFrame(data)
    return df

#get_artist_data(artists_file[0])

# function that takes the xml file and returns a list of the artist dataframes for each 
# artist
def get_all_artists(file):
    df_list = []
    for x in file:        
        df_list.append(get_artist_data(x))
    return df_list

all_artists = get_all_artists(artists_file)

#all_artists[6]

# combine all the artist dataframes into one dataframe
all_artists = pd.concat(all_artists, ignore_index =True, axis=0)

all_artists

all_artists.to_csv('artists_aliases.csv')

# load in our file which includes artist ids, artist names, and aliases
df_artists_aliases = pd.read_csv('artists_aliases.csv')
print(df_artists_aliases.head())

#make a series of the artist ids for those artists we are interested in
series_id = df_cleaned['artistId']
series_id

# create a dataframe of the artists with aliases for only those artists we are interested in
df_reconciled = df_artists_aliases[df_artists_aliases['id'].isin(series_id)]

#df_reconciled = df_reconciled.drop(columns = 'Unnamed: 0')

df_reconciled

# reset the index in the new dataframe
df_reconciled.reset_index(drop=True, inplace=True)

df_reconciled.to_csv('artists_aliases.csv')

#df_edges_names = pd.read_csv('df_edge_list_names.csv')

#df_edges_names.head()

#df_reconciled[df_reconciled['id']==198518]

#df_edge_count = pd.read_csv('edge_count.csv')

#df_edge_count.head()

#df_reconciled.loc[df_reconciled['aliases'].str.contains("331629", case=False)]['id'].to_string(index=False)

# checking whether an artist is shown as sharing an edge with an id associated with one of their own aliases
#def checkAliasCollaborations(edge_list, edge_count):
#    for ind in edge_count.index:
#        value = str(edge_count['V1'][ind])
#        comparison = df_reconciled.loc[df_reconciled['aliases'].str.contains(str(edge_count['V2'][ind]), case=False)]['id'].to_string(index=False)
#        if value == comparison:
#       # Get indices where name column has value from column V1 and value from column V2 where are same artist
#            indexNames = edge_list[(edge_list['V1'] == int(value)) & (edge_list['V2'] == int(edge_count['V2'][ind]))].index
#        # Delete these row indexes from dataFrame
#            edge_list.drop(indexNames , inplace=True)
#    return edge_list

#df_edges_full = pd.read_csv('discogs_edges.csv')
#print("length of df before: ", len(df_edges_full))

# making a dictionary of artist ids and associated aliases
alias_dict = {}
with open('artists_aliases.csv', 'r', encoding="utf8") as file:
    iterator = csv.reader(file)
    for row in iterator:
        artist_id = row[1]
        aliases = row[3]
        alias_dict[artist_id] = aliases

# creating a list of artists that are not collaborating with their own aliases
edges_without_alias_collaboration = []
with open('discogs_edges.csv', 'r', encoding="utf8") as file:
    iterator = csv.reader(file)
    for row in iterator:
       v1, v2 = row
       if v2 not in alias_dict.get(v1,[]):
           edges_without_alias_collaboration.append(row)
                

#for edge in edges_without_alias_collaboration:
##    print(edge)

len(edges_without_alias_collaboration)
df = pd.DataFrame(edges_without_alias_collaboration)
print("length of df after: ", len(df))

df.to_csv('df_edges_cleaned.csv')



#df_edge_latest = checkAliasCollaborations(df_updated_edges, df_edge_count)
#print("length of df after: ", len(df_edge_latest))

# new updated edge list with alias collaborations removed
#df_edge_latest.to_csv('df_edges_cleaned.csv', index = False)

df_edges = pd.read_csv('df_edges_cleaned.csv', index_col=0)

df_edges.head()

df_edges = df_edges.iloc[1:]
df_edges.head()

len(df_cleaned)

combined_nodes = pd.concat([df_edges['0'], df_edges['1']])
combined_nodes = combined_nodes.astype(int)

len(combined_nodes.unique())

# get only the artists that are in the list of nodes from our edge list
df_artists_hh_new = df_cleaned[df_cleaned["artistId"].isin(combined_nodes)]
len(df_artists_hh_new)

# remove the duplicates from the artist list we have just created
#df_artists_cleaned = df_artists_hh_new[~df_artists_hh_new['artistName'].str.lower().duplicated()]

#len(df_artists_cleaned)

#df_artists_cleaned.head()

df_artists_hh_new.to_csv('artists_cleaned_after_duplicates.csv', index = False)

