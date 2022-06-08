# Analyzing topics within songs of the yearly chart rankings in the U.S., U.K. and France

## Dataset
The full dataset, which includes song title, artist, year, raw lyrics, country and detected language is contained in ```lang_lyrics_df.tsv```. It is saved under the tab-separated values format rather than CSV, as song titles or lyrics could contain commas.

## Reproduce the scraping
The script ```scrapping_scripts/scrap_all.py``` can be used to retrieve all lists of songs used in this study as well as their lyrics/

## Topic modeling
The notebook ```topic_modeling.ipynb``` includes all preprocessing and cleaning task, including the language classification, as well as the topic modeling itself and some results analysis.  
The notebook ```alter_methods.ipynb``` takes a look at word search, as an alternative computational method to topic modeling.
