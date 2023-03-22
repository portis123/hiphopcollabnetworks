# -*- coding: utf-8 -*-
"""
Created on Wed Mar 22 18:37:33 2023

@author: Monique Brogan
"""
# Code to gather location data for US artists we are missing from MusicBrainz using the 
# musicbrainzngs library. 
# Source of some of the below code: https://python.hotexamples.com/examples/musicbrainzngs/-/get_artist_by_id/python-get_artist_by_id-function-examples.html

import musicbrainzngs as mbz
import time
import pandas as pd

mbz.set_useragent('MoniqueBrogan', '0.1', '123portis@googlemail.com')

from fuzzywuzzy import process

# getting the name from the list returned by MusicBrainz that most closely matches the artist
# name from Discogs
def check_name_match(artistList, artistName):
    name = artistName
    options = artistList
    # Get a list of matches ordered by match score - printed so can verify it is a good match
    print(process.extract(name, options))
    # Selecting the highest scoring match
    result = process.extractOne(name, options)
    correct_name = result[0]
    print("Correct name: ", correct_name)
    return correct_name

# getting location where artist was born from MusicBrainz and type of artist 
# (person or group)
def get_location_and_type(artist_name):
    try:
        result = mbz.search_artists(artist=artist_name)['artist-list']
        if not result:  
            artist = "no artist returned"
        else:
            names_list = []
            # looping through the artist list returned to get the index and names of artists
            for i in range(len(result)):
                names_list.append(result[i]['name'])
            # get the correct search result from Musicbrainz most closely matching 
            # Discogs artist as per a fuzzy match
            correct_result = check_name_match(names_list, artist_name)
            # index of best match to artist from the names_list
            first = names_list.index(correct_result)
            artist = result[first]
            time.sleep(20)
    except mbz.WebServiceError as exc:
        print("Error encountered: %s" % exc)
        return

    begin_area = get_begin_area(artist)
    typeName = get_type(artist)
    return (begin_area, typeName)


# getting the begin-area of each artist, birthplace for person or place where group formed
def get_begin_area(artistName):
    begin_area = None
    if "begin-area" in artistName and artistName["begin-area"] is not None and "name" in artistName["begin-area"]:
        begin_area = artistName["begin-area"]["name"]
    else:
        begin_area = "not available"
    return begin_area


# getting the type of each artist (person or group)
def get_type(artistName):
    typeName = None
    if "type" in artistName and artistName["type"] is not None:
        typeName = artistName["type"]
    else:
        typeName = "not available"
    return typeName

# adding location and type data to artist dataframe
def add_location_and_type(artist_df):
    for ind in artist_df.index:
        artist = artist_df['artistName'][ind]
        if pd.isnull(artist_df['location'][ind]):
            location, typeName = get_location_and_type(artist)
            print(artist, ": location: ", location, "type: ", typeName)
            artist_df.at[ind,'location'] = location
            artist_df.at[ind,'type'] = typeName
    return artist_df

df_artists_location_needed = pd.read_csv('artists_missing_locations.csv')

df_artists_location_needed.head()

df = add_location_and_type(df_artists_location_needed)