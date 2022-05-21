"""
Clément Dauvilliers - Grenoble INP / EPFL 12/03/2022

Scraps the 50 / 100 best sellings singles between 1994 and 2020 according to the
official SNEP yearly rankings.

"""
import pandas as pd
import requests
import os
import sys
from bs4 import BeautifulSoup
from utils import clean_scrapped_entry


def main():
    # Define the TOP 50 pages URLs
    base_url = "https://snepmusique.com/les-tops/le-top-de-lannee/top-singles-annee/?annee="

    # Step 1: for each year, obtain a pandas dataframe containing the ranking
    yearly_rankings = []
    for year in range(1994, 2021):
        print(f"Processing year {year}")
        # Retrieves the HTML page from the website via http
        url = base_url + f"{year}"
        page = requests.get(url)

        # Parse the HTML content using BeautifulSoup4
        soup = BeautifulSoup(page.content, "html.parser")
        # Retrieves the names of artists and titles from the <div> elements
        # whose class are "artiste" or "titre"
        artists = [div_html.text for div_html in soup.find_all('div', class_='artiste')]
        titles = [div_html.text for div_html in soup.find_all('div', class_='titre')]
        # Retrieves the rank of the song, which we'll use to keep only the top 100
        ranks = [int(div_html.text) for div_html in soup.find_all('div', class_='rang')]
        # Assembles those data into a DataFrame
        songs_data = pd.DataFrame({'artist': artists, 'title': titles, 'rank': ranks})
        # Keeps only singles that are top 100 or better
        songs_data = songs_data[songs_data['rank'] <= 101].drop('rank', axis=1)

        # removes any row in the df that contains an empty element
        songs_data.applymap(lambda val: val if val != '' else None).dropna(inplace=True)
        songs_data = songs_data.applymap(clean_scrapped_entry)

        # Adds the column filled with the current year that is being treated
        # (this column is the same for every song in the df).
        songs_data['year'] = [year for _ in range(len(songs_data))]

        yearly_rankings.append(songs_data)

    final_df = pd.concat(yearly_rankings)
    final_df.to_csv(sys.argv[1], sep='\t')
    return 0


if __name__ == '__main__':
    main()
