# Community Detection in the sphere of US hip hop through the analysis of collaboration networks
Files included in this repository are:

1. GenreLimiter.Rmd: R file where Discogs masters file from 1 September 2018 in xml format is parsed and filtered for entries containing the Hip Hop genre, then with data quality classified as Correct, and removing entries with any other genres in addition to Hip Hop. Lastly, only entries with collaborations are retained, and an edge list of collaborating pairs of artists is created and saved as a csv file
2. discogs_edges.csv: Output of GenreLimiter.Rmd
3. xml_to_artists_df.Rmd: R file where Discogs masters file is used to create a dataframe of artist ids and artist names
4. artists.csv: Output of xml_to_artists_df.Rmd
5. ConvertingEdgeList.py: Python file where an edge list with artist names is created instead of IDs from the original edge list from Discogs, as well as filtering the wider artist list derived from the masters dataset so that it reflects only the collaborating hip hop artists, as reflected in the edge file from GenreLimiter.Rmd
6. df_artists_cleaned.csv: Output of ConvertingEdgeList.py containing artist list filtered to contain relevant collaborating hip hop artists
7. df_edge_list_names.csv: Output of ConvertingEdgeList.py containing edge list created with artist names instead of artist ids
8. GettingAliasesRemovingCollabs.py: Python file where the xmltodict library is used to get details of artists' aliases in a dataframe alongside their artist ids and names from the Discogs artists file from 1 September 2018. Then all instances in the edge list where an artist is shown as collaborating with one of their own aliases is removed. Finally, the artist list is filtered for only those artists remaining in the updated edge list
9. artists_aliases.csv: Output of GettingAliasesRemovingCollabs.py containing artist alias information for artists within collaborating hip hop artists dataset
10. df_edges_cleaned.csv: Output of GettingAliasesRemovingCollabs.py containing edges where artists are not collaborating with one of their aliases
11. artists_cleaned_after_duplicates.csv: Output of GettingAliasesRemovingCollabs.py containing only those artists contained in the updated edge list (df_edges_cleaned.csv)
12. ArtistCountryMusicbrainz.py: Python file where the the country for each artist in the dataset is requested through calls to the MusicBrainz API 
using the musicbrainzngs library
13. artist_id_names_country_mb.csv: File in which country information for artists has been inputted mainly based on requests from MusicBrainz as well as research from other sources
