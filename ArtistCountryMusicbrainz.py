# -*- coding: utf-8 -*-
"""
Created on Wed Mar 22 18:18:52 2023

Getting the country for each artist in the dataset through calls to the MusicBrainz API 
using the musicbrainzngs library. 
Source: https://python.hotexamples.com/examples/musicbrainzngs/-/get_artist_by_id/python-get_artist_by_id-function-examples.html

@author: Monique Brogan
"""

import musicbrainzngs as mbz

mbz.set_useragent('MoniqueBrogan', '0.1', '123portis@googlemail.com')

import time

import pandas as pd

# importing fuzzywuzzy library to help with fuzzy matching of artist names from Discogs 
# with those from MusicBrainz
from fuzzywuzzy import process

# getting the name from the list returned by MusicBrainz that most closely matches the artist 
# name from Discogs
def check_name_match(artistList, artistName):
    name = artistName
    options = artistList
    # Get a list of matches ordered by match score - printed so can verify it is a 
    # good match
    print(process.extract(name, options))
    # Selecting the highest scoring match
    result = process.extractOne(name, options)
    correct_name = result[0]
    print("Correct name: ", correct_name)
    return correct_name


# searching for the artist using MusicBrainz API, then finding their area (usually country)
def get_country(artist_name):
    try:
        result = mbz.search_artists(artist=artist_name)['artist-list']
        if not result:  
            artist = "no artist returned"
        else:
            names_list = []
            # looping through the artist list returned to get the index and names of artists
            for i in range(len(result)):
                names_list.append(result[i]['name'])
            # get the correct search result from MusicBrainz most closely matching our Discogs artist as per a fuzzy match
            correct_result = check_name_match(names_list, artist_name)
            # index of best match to our artist from the names_list
            first = names_list.index(correct_result)
            artist = result[first]
            time.sleep(20)
    except mbz.WebServiceError as exc:
        print("Error encountered: %s" % exc)
        return

    country = None

    if "area" in artist and artist["area"] is not None and "name" in artist["area"]:
                country = artist["area"]["name"]
    else:
        country = "not available"
    return country

# testing function works
get_country("Thomas Mapfumo")

# taking dataframe with artists in it and adding country obtained from MusicBrainz pull
def add_country(artist_df):
    for ind in artist_df.index:
        artist = artist_df['artistName'][ind]
        country = get_country(artist)
        print(artist, ":", country)
        artist_df.at[ind,'country'] = country
    return artist_df

# loading the artist list from cleaned Discogs dataset
df_artists_cleaned = pd.read_csv('artists_cleaned_after_duplicates.csv')

df_artists_cleaned.head()

df = add_country(df_artists_cleaned)

#df.to_csv('artists_cleaned_after_duplicates_country.csv',index = False)