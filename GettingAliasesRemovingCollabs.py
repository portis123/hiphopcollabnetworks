# -*- coding: utf-8 -*-
"""
Used the xmltodict library to get details of artists' aliases in a dataframe alongside their 
artist ids and names. 
Reference: https://python.plainenglish.io/saving-xml-content-to-a-pandas-dataframe-using-xmltodict-b6fab32a5100. 
Then removed all instances from the edge list where an artist is shown as collaborating with themselves.
Cleaned up the artist list based on updated edge list

@author: Monique Brogan
"""
#pip install xmltodict

# to help with decompressing Discogs data dump file
import gzip

import xmltodict
import pandas as pd
import csv

# import list of artist ids and artist names
df_cleaned = pd.read_csv('df_artists_cleaned.csv', index_col=0)

# parsing the Discogs artists file 
artists_file = xmltodict.parse(gzip.GzipFile('discogs_20180901_artists.xml.gz'))

# refining the data to look at the artists
artists_file = artists_file['artists']['artist']

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

# function that takes the xml file and returns a list of the artist dataframes for each artist
def get_all_artists(file):
    df_list = []
    for x in file:        
        df_list.append(get_artist_data(x))
    return df_list

all_artists = get_all_artists(artists_file)

# combine all the artist dataframes into one dataframe
all_artists = pd.concat(all_artists, ignore_index =True, axis=0)

all_artists.to_csv('artists_aliases.csv')

# load in our file which includes artist ids, artist names, and aliases
df_artists_aliases = pd.read_csv('artists_aliases.csv', index_col=0)

#make a series of the artist ids for those artists we are interested in
series_id = df_cleaned['artistId']

# create a dataframe of the artists with aliases for only those artists we are interested in
df_reconciled = df_artists_aliases[df_artists_aliases['id'].isin(series_id)]

# reset the index in the new dataframe
df_reconciled.reset_index(drop=True, inplace=True)

df_reconciled.to_csv('artists_aliases.csv')


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
                

df_edges_before = pd.read_csv('discogs_edges.csv')
len(df_edges_before)
df = pd.DataFrame(edges_without_alias_collaboration)
print("length of df after: ", len(df))

df.to_csv('df_edges_cleaned.csv')

df_edges = pd.read_csv('df_edges_cleaned.csv', index_col=0)

# only look at header and artist Ids, without V1 and V2
df_edges = df_edges.iloc[1:]

combined_nodes = pd.concat([df_edges['0'], df_edges['1']])
combined_nodes = combined_nodes.astype(int)

# number of unique ids from the cleaned edge list
len(combined_nodes.unique())

# get only the artists that are in the list of nodes from our edge list
df_artists_hh_new = df_cleaned[df_cleaned["artistId"].isin(combined_nodes)]
# check number of artists is same as number of unique ids from the cleaned edge list
len(df_artists_hh_new)

df_artists_hh_new.to_csv('artists_cleaned_after_duplicates.csv', index = False)

