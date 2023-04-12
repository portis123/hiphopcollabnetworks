# Community Detection in the sphere of US hip hop through the analysis of collaboration networks
Files included in this repository are:

1. GenreLimiter.Rmd: R file where Discogs masters file from 1 September 2018 in xml format is parsed and filtered for entries containing the Hip Hop genre, then with data quality classified as Correct, and removing entries with any other genres in addition to Hip Hop. Lastly, only entries with collaborations are retained, and an edge list of collaborating pairs of artists is created and saved as a csv file
2. discogs_edges.csv: Output of GenreLimiter.Rmd
3. xml_to_artists_df.Rmd: R file where Discogs masters file is used to create a dataframe of artist ids and artist names
4. artists.csv: Output of xml_to_artists_df.Rmd
3. ConvertingEdgeList.py: Python file where an edge list with artist names is created instead of IDs from the original edge list from Discogs, as well as filtering the wider artist list derived from the masters dataset so that it reflects only the collaborating hip hop artists, as reflected in the edge file from GenreLimiter.Rmd
4. GettingAliasesRemovingCollabs.py: Python file where the xmltodict library is used to get details of artists' aliases in a dataframe alongside their artist ids and names from the Discogs artists file from 1 September 2018. Then all instances in the edge list where an artist is shown as collaborating with one of their own aliases is removed. Finally, the artist list is filtered for only those artists remaining in the updated edge list