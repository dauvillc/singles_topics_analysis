"""
Usage: python3 scrap_lyrics.py <tsv file> <JSON save file path>
the TSV file must include columns 'artist' and 'title'

Clément Dauvilliers - Grenoble INP / EPFL - 12/03/2022

Scraps the lyrics of a list of songs based on the song's artist and title.
The lyrics are obtained from GENIUS.com.
Credits go to https://medium.com/analytics-vidhya/how-to-scrape-song-lyrics-a-gentle-python-tutorial-5b1d4ab351d2
"""
import pandas as pd
import sys
from tqdm import tqdm
from lyricsgenius import Genius

# Client access token from the GENIUS.com API
GENIUS_API_TOKEN = 'HAZ_eq6H-8t0a0Gxy6OJgbJbkcngxKjw5R5nL0a2pFy9HI9dhK1k-Ff9ZTvuPqAu'


def main():
    songs_list = pd.read_csv(sys.argv[1], sep="\t")[['artist', 'title', 'year']]
    songs_list['artist'] = songs_list['artist'].apply(lambda s: str(s).lower())
    songs_list['title'] = songs_list['title'].apply(lambda s: str(s).lower())

    genius = Genius(GENIUS_API_TOKEN)
    genius.remove_section_headers = True
    genius.skip_non_songs = True

    songs_lyrics, lyrics_states, songs_years = [], [], []
    skipped_songs_artists, skipped_songs_titles = [], []
    for index, song_data in tqdm(songs_list.iterrows(), total=songs_list.shape[0]):
        try:
            song_info = genius.search_song(title=song_data['title'],
                                           artist=song_data['artist'])
            songs_lyrics.append(song_info.lyrics)
            lyrics_states.append(song_info.lyrics_state)
        except:
            skipped_songs_titles.append(song_data['title'])
            skipped_songs_artists.append(song_data['artist'])
            songs_lyrics.append(None)
            lyrics_states.append("missing")
            continue

    songs_list['lyrics'] = songs_lyrics
    songs_list['lyrics_state'] = lyrics_states
    songs_list.to_json(sys.argv[2])

    return 0


if __name__ == "__main__":
    main()
