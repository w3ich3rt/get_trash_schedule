#!/usr/bin/env python3
""" Purpose: This script pulls the ICS calendar file and parses the
    dates and waste types for further processing.

    Author: Ulli Weichert (ulli@weichert.it)
    Date: 03.02.2023
"""

# IMPORTS

from os import path
from ics import Calendar, Event
import requests

# CLASSES


class GetTheCalenderFile():
    """Download, Read and Delete the file"""
    req = ""
    _file = "abfuhrplan2023.ics"

    def __init__(self, _target_url) -> None:
        self.req = requests.get(_target_url, timeout=5)

    def write_file(self, filename: str = _file) -> str:
        """Write the calendar file to disk."""
        if path.exists(filename):
            print("File exists already... skipping download.")
        else:
            with open(filename, 'w', encoding='utf8') as file:
                file.write(self.req.text)
        return filename
    
    def read_file(self, filename: str = _file) -> list:
        """Read the calendar file"""
        with open(filename, 'r', encoding="utf8") as file:
            text = file.read()
        return text

    def parse_file(self, filename: str = _file) -> list:
        """Parse the calendar file"""
        __list = []
        cals = Calendar(self.read_file(filename))
        for event in cals.events:
            __item = [event.name, str(event.begin)]
            __list.append(__item)
        return __list


# FUNCTIONS

# VARIABLES
URL = "https://abfallkalender.regioit.de/kalender-pi/downloadfile.jsp?format=ics&jahr=2023&ort=Bokholt-Hanredder&strasse=11054165&fraktion=0&fraktion=1&fraktion=2&fraktion=4&fraktion=5&fraktion=7&fraktion=9"

# MAIN CODE


def main():
    """main function"""
    ics = GetTheCalenderFile(URL)
    events = ics.parse_file()

    for event in events:
        if "Biotonne" in event:
            print(event)

if __name__ == '__main__':
    main()
