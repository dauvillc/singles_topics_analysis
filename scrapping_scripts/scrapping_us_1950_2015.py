"""
Usage: python3 scrapping_us_1950_2015.py <destination_file.csv>

Clément Dauvilliers - EPFL - 03/05/2022

Extracts the songs (artiste, title, year) from the Billboard top 100, scrapped by
Kevin Schaich (MIT).
"""
import os
import sys
import pandas as pd

# Repertory in which the top 100 lists for 1950-2015 are saved.
SONGS_LISTS_DIR = "data/billboard_data/top100"

if __name__ == "__main__":
    yearly_dfs = []
    for year in range(1950, 2016):
        # Reads the data for every song of the current year, and keeps only
        # the artist, and title
        year_songs = pd.read_csv(os.path.join(SONGS_LISTS_DIR, f'{year}.csv'),
                                 encoding_errors='ignore')
        year_songs = year_songs[['Artist', 'Song Title']].rename({'Artist': 'artist', 'Song Title': 'title'},
                                                                 axis=1)
        # Adds a column to indicate the year
        year_songs['year'] = [year for _ in range(year_songs.shape[0])]

        yearly_dfs.append(year_songs)
        print(f"Processed year {year}")

    # Compiles all years together
    final_df = pd.concat(yearly_dfs)
    # Saves the result to the destination file
    final_df.reset_index(drop=True).to_csv(sys.argv[1], sep='\t')
