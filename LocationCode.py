# -*- coding: utf-8 -*-
"""
Created on Thu Mar 30 19:46:17 2023

@author: Monique Brogan

Adding location classifiers, the basis for ground truth, to artist details

"""

import pandas as pd

df_artists = pd.read_csv('artists_with_classification_cleaned.csv', index_col= 0)
print(df_artists['Code'])

df_artists = df_artists.assign(Code='')
df_artists['Code']

length_before = len(df_artists)

def classifyArtistLocation(df_artists):
    for ind, val in df_artists['Classification'].iteritems():
        listOfCodes = []
        if "East Coast" in val:
            listOfCodes.append(1)
        if "Midwest" in val:
            listOfCodes.append(2)
        if "Southern" in val:
            listOfCodes.append(3)
        if "West Coast" in val:
            listOfCodes.append(4)
        if "Hawaii" in val:
            listOfCodes.append(5)
        df_artists.at[ind, 'Code'] = listOfCodes
        #df_artists.loc[ind, 'Code'] = pd.Series(listOfCodes)
        #print(df_artists.loc[ind, 'Code'])
    return
        
classifyArtistLocation(df_artists)
        
list(df_artists.columns)
print(df_artists['Code'])
length_after = len(df_artists)

#df_artists = df_artists.loc[:, ~df_artists.columns.str.contains('^Unnamed')]
#list(df_artists.columns)
#print(df_artists)
assert(length_before == length_after)


df_artists.to_csv('artists_with_location_codes_simpler.csv')
    