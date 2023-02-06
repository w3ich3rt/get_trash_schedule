#!/usr/bin/env python3
""" Purpose: This script pulls the ICS calendar file and parses the
    dates and waste types for further processing.

    Author: Ulli Weichert (ulli@weichert.it)
    Date: 03.02.2023
"""

# IMPORTS

from os import path
import datetime
from ics import Calendar
import requests

# CLASSES


class GetTheCalenderFile():
    """Download, Read and Delete the file"""

    _file = "abfurhplan.ics"

    def __init__(self, _target_url, file: str = _file) -> None:
        if path.exists(file):
            print("File exists already... skipping download.")
        else:
            with open(file, 'w', encoding='utf8') as file:
                self._req = requests.get(_target_url, timeout=15)
                self.write_file()

    def write_file(self, filename: str = _file) -> str:
        """Write the calendar file to disk."""
        with open(filename, 'w', encoding='utf8') as file:
            file.write(self._req.text)
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
            __item = [event.name, str(event.begin)[:10]]
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
    currentdate = datetime.datetime.now().date()
    twodaysago = currentdate + datetime.timedelta(days=1)

    for event in events:
        if str(twodaysago) in event:
            return_msg = {
                'msg': f"Morgen ist {event[0]}."
            }
    return return_msg


if __name__ == '__main__':
    main()
