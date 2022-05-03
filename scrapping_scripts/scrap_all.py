"""
Clément Dauvilliers - EPFL - 03/05/2022
Assembles the full dataset at once by combining all scapping scripts.
"""
import os

_SINGLES_REP = "data/singles_lists"
_DEST_REP = "data/lyrics"
_FINAL_FILE = "data/all_lyrics.json"

if __name__ == "__main__":
    lists_names = ['fr_1970_1984', 'fr_1985_1993', 'fr_1994_2020',
                   'uk_1953_2004', 'uk_2005_2020']

    # STEP 1: Retrieve the charts singles lists from the websites
    for name in lists_names:
        print(f"Searching for {_SINGLES_REP}/top_{name}.tsv")
        if not os.path.exists(os.path.join(_SINGLES_REP, f"top_{name}.tsv")):
            print("Not found")
            os.system(f"python3 scrapping_scripts/scrapping_{name}.py {_SINGLES_REP}/top_{name}.tsv")
        else:
            print("Found")

    # STEP 2: Scrap the lyrics
    for name in lists_names:
        print(f"Searching for {_DEST_REP}/{name}.json")
        if not os.path.exists(os.path.join(_DEST_REP, f"{name}.json")):
            print("Not found")
            list_file = os.path.join(_SINGLES_REP, f"top_{name}.tsv")
            dest_file = os.path.join(_DEST_REP, f"{name}.json")
            os.system(f"python3 scrapping_scripts/scrap_lyrics.py {list_file} {dest_file}")
        else:
            print("Found")

    # STEP 2.5: Treatment for the US data which doesn't need to be webscrapped
    os.system(f"python3 scrapping_scripts/scrapping_us_1950_2015.py {_DEST_REP}/us_1950_2015.json")

    # STEP 3: merge
    os.system(f"python3 scrapping_scripts/merge_datasets {_FINAL_FILE} {_DEST_REP}")