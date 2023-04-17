# Community Detection in the sphere of US hip hop through the analysis of collaboration networks

Analysis is based on the Discogs masters data dump from 1 September 2018 (https://dataverse.harvard.edu/file.xhtml?persistentId=doi:10.7910/DVN/Q02JJQ/Y6C9UK&version=2.0), and also uses the Discogs artists data dump from the same date (https://discogs-data-dumps.s3.us-west-2.amazonaws.com/index.html?prefix=data/2018/).

Files included in this repository are:

1. [GenreLimiter.Rmd](GenreLimiter.Rmd): R file where the Discogs masters file from 1 September 2018 in xml format is parsed and filtered for entries containing the Hip Hop genre, then with data quality classified as Correct, and removing entries with any other genres in addition to Hip Hop. Lastly, only entries with collaborations are retained, and an edge list of collaborating pairs of artists is created and saved as a csv file
    * [discogs_edges.csv](discogs_edges.csv): Output of GenreLimiter.Rmd - edge list of collaborating pairs of artists
2. [XMLToArtistsDf.Rmd](XMLToArtistsDf.Rmd): R file where Discogs masters file is used to create a dataframe of artist ids and artist names
    *  [artists.csv](artists.csv): Output of XMLToArtistsDf.Rmd - artist ids and artist names 
3. [ConvertingEdgeList.py](ConvertingEdgeList.py): Python file where an edge list with artist names is created instead of IDs from the original edge list from Discogs, as well as filtering the wider artist list derived from the masters dataset so that it reflects only the collaborating hip hop artists, as reflected in the edge file from GenreLimiter.Rmd
    *  [df_artists_cleaned.csv](df_artists_cleaned.csv): Output of ConvertingEdgeList.py containing artist list filtered to contain relevant collaborating hip hop artists
    *  [df_edge_list_names.csv](df_edge_list_names.csv): Output of ConvertingEdgeList.py containing edge list created with artist names instead of artist ids
4. [GettingAliasesRemovingCollabs.py](GettingAliasesRemovingCollabs.py): Python file where the xmltodict library is used to get details of artists' aliases in a dataframe alongside their artist ids and names from the Discogs artists file from 1 September 2018. Then all instances in the edge list where an artist is shown as collaborating with one of their own aliases is removed. Finally, the artist list is filtered for only those artists remaining in the updated edge list
    * [artists_aliases.csv](artists_aliases.csv): Output of GettingAliasesRemovingCollabs.py containing artist alias information for artists within collaborating hip hop artists dataset
    * [df_edges_cleaned.csv](df_edges_cleaned.csv): Output of GettingAliasesRemovingCollabs.py containing edges where artists are not collaborating with one of their aliases
    * [artists_cleaned_after_duplicates.csv](artists_cleaned_after_duplicates.csv): Output of GettingAliasesRemovingCollabs.py containing only those artists contained in the updated edge list (df_edges_cleaned.csv)
5. [ArtistCountryMusicbrainz.py](ArtistCountryMusicbrainz.py): Python file where the the country for each artist in the dataset is requested through calls to the MusicBrainz API using the musicbrainzngs library
    * [artist_id_names_country.csv](artist_id_names_country.csv): File in which country information for artists has been inputted mainly based on requests from MusicBrainz as well as research from other sources. Used in Excel format but saved as csv to be compatible with Github requirements
6. [USOnlyData.py](USOnlyData.py): Python file where the dataset is filtered for artists based in the US only
    * [edges_us_only.csv](edges_us_only.csv): Output of USOnlyData.py. Edge file for collaborating artists from the US only
    * [artists_us_only.csv](artists_us_only.csv): Output of USOnlyData.py. US artists only
    * [artists_missing_locations.csv](artists_missing_locations.csv): Output of USOnlyData.py. US artists missing locations
7. [LocationTypeMusicBrainz.py](LocationTypeMusicBrainz.py): Python file where the the begin area and type for each artist in the dataset is requested through calls to the MusicBrainz API using the musicbrainzngs library
    * [artists_us_only_w_location.csv](artists_us_only_w_location.csv): File in which location and type information for artists has been inputted mainly based on requests from MusicBrainz as well as research from other sources. Used in Excel format but saved as csv to be compatible with Github requirements
8. [RemovingArtists.py](RemovingArtists.py): Python file where artists that have been marked to remove because of being labels rather than artists, having incorrect 
country data (not US - found when adding locations) or not being musicians but rather actors (Saget) or other non-musicians (Malcolm X), are removed
    * [edges_us_only_cleaned.csv](edges_us_only_cleaned.csv): Output of RemovingArtists.py. Updated edge list without removed artists
    * [artists_us_only_cleaned.csv](artists_us_only_cleaned.csv): Output of RemovingArtists.py. Updated artist list without removed artists
9. [RemovingArtistsWoLocations.py](RemovingArtistsWoLocations.py): Python file where artists that have no location (not able to be found) are removed frpm the edge file and artist file
    * [edges_with_locations.csv](edges_with_locations.csv): Output of RemovingArtistsWoLocations.py. Updated edge list with artists with no locations removed
    * [artists_with_classification_cleaned.csv](artists_with_classification_cleaned.csv): Output of RemovingArtistsWoLocations.py. Updated artist list with artists with no locations removed. Afterwards, cleaned up locations and classifications to avoid misspellings etc in Excel
10. **The remove tag was added in the Excel file manually for those artists with multiple locations, and the RemovingArtists.py functionality was used again to remove these artist from the dataset. Output files of this process are below**
    * [edges_w_locations_removed_multiple.csv](edges_w_locations_removed_multiple.csv): Output of running RemovingArtists.py functionality on latest edge file, to remove artists with multiple locations who had been tagged with REMOVE. Edge file resulting from this process
    * [artists_w_locations_removed_multiple.csv](artists_w_locations_removed_multiple.csv): Output of running RemovingArtists.py functionality on latest artist file, to remove artists with multiple locations who had been tagged with REMOVE. Artist file resulting from this process
11. [LocationCode.py](LocationCode.py): Python file where location classifiers are added for artist details, the basis for ground truth
    * [artists_with_location_codes_simpler.csv](artists_with_location_codes_simpler.csv): Output of running LocationCode.py on artist file. Updated artist file
12. [CountEdges.py](CountEdges.py): Python file where the number of edges between the same two artists is counted. Getting edge weight information
    * [edge_count.csv](edge_count.csv): Output of CountEdges.py. Edge weight information
13. [NetworkAnalysis.py](NetworkAnalysis.py): Python file where network analytics are run on the US hip hop artists weighted edge list
14. [CommunitiesTests.py](CommunitiesTests.py): Python file where the Louvain and Leiden Community Detection algorithms are run, along with obtaining their modularity scores to get a comparison of performance
15. [LouvainCommunityDetection.py](LouvainCommunityDetection.py): Python file where the communities produced by the Louvain Community Detection algorithm are plotted
16. [ExaminingCommunities.py](ExaminingCommunities.py): Python file in which the details of communities are examined, looking at all the communities and then the 5 largest by size for location trends. Also looking at 5 largest communities and location trends for top 5 artists in each community by weighted degree
