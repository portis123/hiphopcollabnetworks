# -*- coding: utf-8 -*-
"""
Getting the country for each artist in the dataset through calls to the MusicBrainz API 
using the musicbrainzngs library. 
Reference: https://python.hotexamples.com/examples/musicbrainzngs/-/get_artist_by_id/python-get_artist_by_id-function-examples.html

@author: ##
"""

import musicbrainzngs as mbz

mbz.set_useragent('##', '##', '##')

import time

import pandas as pd

# importing process function from fuzzywuzzy library to help with fuzzy matching of artist names from Discogs 
# with those from MusicBrainz
from fuzzywuzzy import process

# getting the name from the list returned by MusicBrainz that most closely matches the artist name from Discogs
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


# taking dataframe with artists in it and adding country obtained from MusicBrainz pull - in the end, I had to manually add this
# to an Excel file from the printouts rather than allowing the function to add it due to some artists having the same names 
# so data needed to be checked, and I also needed to source data for artists which had no country in MusicBrainz
def add_country(artist_df):
    for ind in artist_df.index:
        artist = artist_df['artistName'][ind]
        country = get_country(artist)
        print(artist, ":", country)
        artist_df.at[ind,'country'] = country
    return artist_df

# loading the artist list from cleaned Discogs dataset
df_artists_cleaned = pd.read_csv('artists_cleaned_after_duplicates.csv')

df = add_country(df_artists_cleaned)