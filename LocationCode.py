# -*- coding: utf-8 -*-
"""
Created on Thu Mar 30 19:46:17 2023

Adding location classifiers, the basis for ground truth, to artist details

@author: Monique Brogan

"""

import pandas as pd

df_artists = pd.read_csv('artists_w_locations_removed_multiple.csv', index_col= 0)
print(df_artists['Code'])

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
        #df_artists.loc[ind, 'Code'] = pd.Series(listOfCodes)
        #print(df_artists.loc[ind, 'Code'])
    return
        
classifyArtistLocation(df_artists)


#list(df_artists.columns)
print(df_artists['Code'])


df_artists.to_csv('artists_with_location_codes_simpler.csv')

print(df_artists['Code'].value_counts())


    