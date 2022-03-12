"""
Clément Dauvilliers - Grenoble INP / EPFL 12/03/2022

Scraps the 50 best selling singles in France for each year between
1985 and 1993 from https://tubesenfrance.com/. The ranking is the
hitparade ranking. The official SNEP Top 50 ranking already existed back then,
but the SNEP website does not give a yearly ranking of sells.
Another more complex method would be to aggregate the weekly SNEP rankings into yearly
results.
"""
import pandas as pd
import requests
import os
from bs4 import BeautifulSoup
from utils import clean_scrapped_entry


def main():
    # Define the TOP 50 pages URLs
    base_url = "https://tubesenfrance.com/annees-"

    # Step 1: for each year, obtain a pandas dataframe containing the ranking
    yearly_rankings = []
    for year in range(1985, 1994):
        print(f"Processing year {year}")
        # Retrieves the HTML page from the website via http
        # the full url is "website.com/annees-[80|90]/classements-de-[annee]/
        url = base_url + f"{int((year - 1900)/10)}0/classements-de-{year}/"
        page = requests.get(url)

        # Parse the HTML content using BeautifulSoup4
        soup = BeautifulSoup(page.content, "html.parser")
        # retrieves the table contained in the "entry-content" div element
        table_html = soup.find(class_="entry-content").find('table')
        # retrieves the list of all rows in the table
        songs_html = table_html.find_all('tr')
        # splits the rows into cells
        songs_data = [[song_feature.text for song_feature in song.find_all('td')] for song in songs_html]
        # converts it to a dataframe, drops the first row which is the table header
        songs_data = pd.DataFrame(songs_data, columns=['position', 'artist', 'title'])
        songs_data.drop(0, inplace=True)
        # removes any row in the df that contains an empty element
        songs_data.applymap(lambda val: val if val != '' else None).dropna(inplace=True)
        songs_data = songs_data.applymap(clean_scrapped_entry)

        # Adds the column filled with the current year that is being treated
        # (this column is the same for every song in the df).
        songs_data['year'] = [year for _ in range(len(songs_data))]

        yearly_rankings.append(songs_data)

    final_df = pd.concat(yearly_rankings)
    final_df.to_csv(os.path.join("data", f"top_fr_1985_1993.tsv"), sep='\t')
    return 0


if __name__ == '__main__':
    main()
