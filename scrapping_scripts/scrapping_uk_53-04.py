"""
Clément Dauvilliers - Grenoble INP / EPFL 24/03/2022

Scraps the TOP100 singles for every week in the UK from the Official Charts Company
(OCC) website. The top 100 is then aggregated into a yearly ranking.
"""
import pandas as pd
import requests
import os
from bs4 import BeautifulSoup
from utils import clean_scrapped_entry
from dateutil import rrule
from datetime import date


def aggregate_weekly_rankings(songs, artists, positions):
    """
    Aggregates the weekly rankings into a single list. The method is the following:
    * Spending 1 week as top 1 gains 100 points
    * Spending 2 weeks as top 2 gains 99, ..
    * Spending k weeks as top k gains 100 - k + 1 points
    :param songs: list of all songs in every week, concatenated into one list
    :param artists: list of all artists in every week, concatenated
    :param positions: positions of every during every week, concatenated
    :return: a pandas DataFrame giving the aggregated ranking.
    """
    weekly_df = pd.DataFrame({"title": songs, "artist": artists, "position": positions})
    weekly_df['week_score'] = 100 - weekly_df['position']
    year_scores = weekly_df.groupby(['title', 'artist']).sum().reset_index()
    top_songs = year_scores.sort_values('week_score', ascending=False).iloc[:100].reset_index()
    top_songs = top_songs.drop('week_score', axis=1)
    top_songs['position'] = [i for i in range(top_songs.shape[0])]
    return top_songs


def main():
    # Define the TOP 50 pages URLs
    base_url = "https://www.officialcharts.com/charts/singles-chart/"

    # Process for each year
    yearly_rankings = []
    for year in range(1953, 2005):
        print(f"Processing year {year}")
        first_week = date.fromisocalendar(year, 1, 1)
        last_week = date.fromisocalendar(year, 52, 1)
        year_artists, year_songs, year_positions = [], [], []

        for dt in rrule.rrule(rrule.WEEKLY, dtstart=first_week, until=last_week):
            print(f"Processing {dt}")
            # Retrieves the HTML page from the website via http
            # The URL is base_url + YYYYMMDD/7501/
            url = base_url + f"{dt.strftime('%Y%m%d')}" + "/7501/"
            page = requests.get(url)

            # Parse the HTML content using BeautifulSoup4
            soup = BeautifulSoup(page.content, "html.parser")
            # Retrieves the artists and songs
            artists = [elem.text.strip().lower() for elem in soup.find_all(class_="artist")]
            songs = [elem.text.strip().lower() for elem in soup.find_all(class_="title")]
            # Position of every song in this week's ranking
            positions = [i for i in range(len(songs))]

            # Adds this week's data to the lists for the current year
            year_artists += artists
            year_songs += songs
            year_positions += positions

        # Aggregates the weekly rankings into the list for the current year
        year_top100 = aggregate_weekly_rankings(year_songs,
                                                year_artists,
                                                year_positions)
        year_top100['year'] = [year for _ in range(year_top100.shape[0])]
        yearly_rankings.append(year_top100)

    final_df = pd.concat(yearly_rankings, axis=0).reset_index()
    final_df.to_csv(os.path.join("data", f"top_uk_1953_2004.tsv"), sep='\t')
    return 0


if __name__ == '__main__':
    main()
