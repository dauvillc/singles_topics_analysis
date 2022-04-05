"""
Clément Dauvilliers - Grenoble INP / EPFL 28/03/2022

Scraps the Top100 End-of-year singles from the Official Charts Company
website.
"""
import pandas as pd
import requests
import os
from bs4 import BeautifulSoup
from utils import clean_scrapped_entry


def main():
    # Define the TOP 50 pages URLs
    base_url = "https://www.officialcharts.com/charts/end-of-year-singles-chart/"

    # Step 1: for each year, obtain a pandas dataframe containing the ranking
    yearly_rankings = []
    for year in range(2005, 2021):
        print(f"Processing year {year}")
        # Retrieves the HTML page from the website via http
        # The URL base_url + YYYY0130/37501 will automatically point towards
        # the ranking for year YYYY
        url = base_url + f"{year}0130/37501/"
        page = requests.get(url)

        # Parse the HTML content using BeautifulSoup4
        soup = BeautifulSoup(page.content, "html.parser")

        # Retrieves the artists and songs
        artists = [elem.text.strip().lower() for elem in soup.find_all(class_="artist")]
        songs = [elem.text.strip().lower() for elem in soup.find_all(class_="title")]
        # Position of every song in this week's ranking
        positions = [i for i in range(len(songs))]

        songs_data = pd.DataFrame({'position': positions, 'artist': artists,
                                   'title': songs})
        # removes any row in the df that contains an empty element
        songs_data.applymap(lambda val: val if val != '' else None).dropna(inplace=True)
        songs_data = songs_data.applymap(clean_scrapped_entry)

        # Adds the column filled with the current year that is being treated
        # (this column is the same for every song in the df).
        songs_data['year'] = [year for _ in range(len(songs_data))]

        yearly_rankings.append(songs_data)

    final_df = pd.concat(yearly_rankings)
    final_df.to_csv(os.path.join("data", f"top_uk_after2005.tsv"), sep='\t')
    return 0


if __name__ == '__main__':
    main()
