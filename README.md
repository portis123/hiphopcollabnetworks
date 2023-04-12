# Community Detection in the sphere of US hip hop through the analysis of collaboration networks
Files included in this repository are:

1. GenreLimiter.Rmd: R file where Discogs masters file in xml format is parsed and filtered for entries containing the Hip Hop genre, then with data quality classified as Correct, and removing entries with any other genres in addition to Hip Hop. Lastly, only entries with collaborations are retained, and an edge list of collaborating pairs of artists is created and saved as a csv file
2. xml_to_artists_df.Rmd: R file where Discogs masters file is used to create a dataframe of artist ids and artist names
