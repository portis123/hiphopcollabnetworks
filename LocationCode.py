# -*- coding: utf-8 -*-
"""
Adding location classifiers, the basis for ground truth, to artist details

@author: ##
"""
import pandas as pd

df_artists = pd.read_csv('artists_w_locations_removed_multiple.csv', index_col= 0)

# make Code column blank so can add location classifier in there
df_artists = df_artists.assign(Code='')
df_artists['Code']

def classifyArtistLocation(df_artists):
    for ind, val in df_artists['Classification'].iteritems():
        if "East Coast" in val:
            df_artists.at[ind, 'Code'] = 1
        if "Midwest" in val:
            df_artists.at[ind, 'Code'] = 2
        if "Southern" in val:
            df_artists.at[ind, 'Code'] = 3
        if "West Coast" in val:
            df_artists.at[ind, 'Code'] = 4
    return
        
classifyArtistLocation(df_artists)

print(df_artists['Code'])

# getting a count of each location classification
print(df_artists['Code'].value_counts())

df_artists.to_csv('artists_with_location_codes_simpler.csv')




    