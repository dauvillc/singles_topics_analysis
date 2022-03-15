"""
Clément Dauvilliers - Grenoble INP / EPFL 12/03/2022

Defines some utility functions used to clean the scrapped data.
"""


def clean_scrapped_entry(str_entry):
    """
    Cleans a string-type text item scrapped from the charts
    webpages.
    Removes the leading and trailing whitespaces and tabulations.
    :param str_entry: string text item.
    :return: the cleaned item.
    """
    return str(str_entry).lstrip().strip().replace('\t', ' ')
