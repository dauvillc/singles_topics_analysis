"""
Usage: python3 scrap_lyrics.py <tsv file>
the TSV file must have the following layout: index artist title

Clément Dauvilliers - Grenoble INP / EPFL - 12/03/2022

Scraps the lyrics of a list of songs based on the song's artist and title.
The lyrics are obtained from GENIUS.com.
Credits go to https://medium.com/analytics-vidhya/how-to-scrape-song-lyrics-a-gentle-python-tutorial-5b1d4ab351d2
"""
import requests
from bs4 import BeautifulSoup
import os
import re


# Client access token from the GENIUS.com API
GENIUS_API_TOKEN = 'HAZ_eq6H-8t0a0Gxy6OJgbJbkcngxKjw5R5nL0a2pFy9HI9dhK1k-Ff9ZTvuPqAu'


def main():
    return 0


if __name__ == "__main__":
    main()
