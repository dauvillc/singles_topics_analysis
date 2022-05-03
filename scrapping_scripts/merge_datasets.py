"""
Usage: python3 merge_datasets.py <dest file> <lyrics files repertory>
Clément DAUVILLIERS 30/04/2022 - EPFL

Merges the lyrics datasets obtained via the scrapping scripts.
The second argument is a repertory under which should be directly put all lyrics files in
the JSON format.
Each filename must be under the form
countrycode_startyear_lastyear.json, such as "fr_70_84.json". The years are indicated as their
last two digits. Possible country codes are uk, us, fr.
"""
import sys
import os
import pandas as pd


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 merge_datasets.py <dest file> <lyrics files repertory>")
        sys.exit(1)
    data_rep = sys.argv[2]

    dataframes = []
    for json_file in os.listdir(data_rep):
        # Reads the json file and forces the following columns order
        data = pd.read_json(os.path.join(data_rep, json_file))[['year', 'artist', 'title', 'lyrics', 'lyrics_state']]
        # Adds a column to indicate the corresponding country
        # using the country code (first two characters in the filename).
        data['country'] = json_file[:2].lower()
        dataframes.append(data)

    # Compiles all datasets together
    merged_df = pd.concat(dataframes).reset_index(drop=True)
    merged_df.to_json(sys.argv[1])