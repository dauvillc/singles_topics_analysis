"""
Clément Dauvilliers - Grenoble INP / EPFL 11/03/2022
Scraps the TOP 100 best selling singles for each year between 1968 and 1984 from
http://chartssinglestop40france.blogspot.com/
"""
import pandas as pd
import requests
import sys
from bs4 import BeautifulSoup
from utils import clean_scrapped_entry


def main():
    # Define the TOP 100 pages URLs
    base_url = "http://chartssinglestop40france.blogspot.com/p/"

    # Step 1: for each year, obtain a pandas dataframe containing the ranking
    yearly_rankings = []
    for year in range(1970, 1985):
        print(f"Processing year {year}")
        # Retrieves the HTML page from the website via http
        # for some reason, the right page for year 1981 is "[base_url]/1981_6.html"
        # instead of "[base_url]/1981.html"
        if year == 1981:
            url = base_url + '1981_6.html'
        else:
            url = base_url + f"{year}.html"
        page = requests.get(url)

        # Parse the HTML content using BeautifulSoup4
        soup = BeautifulSoup(page.content, "html.parser")
        # retrieves the table contained in the "post-body entry-content" div element
        table_html = soup.find(class_="post-body entry-content").find('table')
        # retrieves the list of all rows in the table
        songs_html = table_html.find_all('tr')
        # splits the rows into cells
        songs_data = [[song_feature.text for song_feature in song.find_all('td')] for song in songs_html]
        # converts it to a dataframe, drops the first row which is the table header
        songs_data = pd.DataFrame(songs_data, columns=['artist', 'title', 'date', 'best rank', 'weeks'])
        songs_data.drop(0, inplace=True)
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
