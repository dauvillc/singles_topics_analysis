"""
Usage: python3 scrapping_us_1950_2015.py <destination_file.json>

Clément Dauvilliers - EPFL - 03/05/2022

Extracts the songs (artiste, title, year, lyrics) from the Billboard top 100, scrapped by
Kevin Schaich (MIT).
"""
import os
import sys
import pandas as pd


# Repertory in which the lyrics for every song for each year are saved.
# Contains a single json file for each year (e.g. 1953.json).
DATA_DIR = "data/billboard_data"


if __name__ == "__main__":
    yearly_dfs = []
    for year in range(1950, 2016):
        # Reads the data for every song of the current year, and keeps only
        # the artist, year, title and lyrics
        year_songs = pd.read_json(os.path.join(DATA_DIR, f'{year}.json'))
        year_songs = year_songs[['artist', 'title', 'lyrics', 'year']]

        yearly_dfs.append(year_songs)
        print(f"Processed year {year}")

    # Compiles all years together
    final_df = pd.concat(yearly_dfs)
    # Adds a "lyrics state" column to be coherent with the other
    # datasets (UK and France). In the other datasets, this column
    # indicates whether the lyrics are complete, which is always the case
    # here.
    final_df['lyrics_state'] = ['complete' for _ in range(final_df.shape[0])]
    final_df.reset_index(drop=True).to_json(sys.argv[1])


