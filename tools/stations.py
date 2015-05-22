"""Parse the Deutscher Wetterdienst (DWD) weather station file."""

import json
import logging
import re


class StationEntriesError(Exception):
    pass


def station_file2dict(filepath):
    """Parse weather station file into a dictionary.

    Input station file
    ------------------
    * It has 2 header lines,
    * then follows one line for each weather station and each line has 8
      white space separated entries:

        Field name        Type    Comment
        ----------        ----    -------
        Stations_id       int
        von_datum         int
        bis_datum         int
        Stationshoehe     int     treated as float
        geoBreite         float
        geoLaenge         float
        Stationsname      str     can contain white space
        Bundesland        str     without white space

    Returned dictionary
    -------------------
    Each weather station entry is stored in a dictionary, where the
    'Stations_id' is the key and the value is another dictionary with the
    remaining 7 data fields with data types according to the above table.
    """
    station_dict = {}
    entries_per_station = 8
    header_lines = 2

    # Attention! The textfile given by the DWD is encoded in Latin-1.
    # Python3 uses UTF-8 by default, so we have to specify it here.
    # In Python2 none of this will work, the open() function doesn't
    # even accept encode= as a parameter.
    lines = file2list(filepath, 'Latin-1')

    if lines:
        # Delete the header lines, which we don't need.
        for _ in range(header_lines):
            del lines[0]

        for n, line in enumerate(lines):
            wordlist = re.sub("[\s]", " ",  line).split()
            logging.debug(wordlist)

            # Some Stationsname have spaces in them, e.g "Nordseeboje 2" (yes,
            # this station is in the water!). Join the list entries to preserve
            # this. Note that no Bundesland has spaces in the name, which
            # simplify things.
            if entries_per_station < len(wordlist):
                wordlist[6] = " ".join(wordlist[6:-1])
                del wordlist[7:-1]
            nwords = len(wordlist)
            if nwords != entries_per_station:
                raise StationEntriesError(("wrong number of entries"
                                           " on line %d") % n+header_lines+1)

            # XXX Use float for Stationshoehe even if we are only provided with
            # integer precision right now. A height is a decimal number.
            station_dict[int(wordlist[0])] = {'von_datum': int(wordlist[1]),
                                              'bis_datum': int(wordlist[2]),
                                              'Stationshoehe':
                                              float(wordlist[3]), 'geoBreite':
                                              float(wordlist[4]), 'geoLaenge':
                                              float(wordlist[5]),
                                              'Stationsname': wordlist[6],
                                              'Bundesland': wordlist[7]}

    return station_dict


def file2list(filepath, enc='UTF-8', mode='rt'):
    """Read file content to list."""
    lines = []

    with open(filepath, mode, encoding=enc) as fd:
        lines = fd.readlines()

        # The TU_Stundenwerte_Beschreibung_Stationen.txt file has an EOF
        # marker.
        if lines[-1] == '\x1a':
            logging.debug("removing EOF marker")
            del lines[-1]

    return lines


def dump_dict2json(d, filepath):
    """Dump dictionary to JSON file."""
    with open(filepath, 'w', encoding='UTF-8') as json_file:
        json_file.write(get_pretty_json(d))


def get_pretty_json(json_obj):
    """JSON encode argument in pretty format."""
    return json.dumps(json_obj, sort_keys=True,
                      indent=4, separators=(',', ': '))


def load_int_key_json2dict(f):
    """Read JSON file to dict, converting keys to int."""
    d = {}
    with open(f, 'r', encoding='UTF-8') as json_file:
        d = {int(k): v for k, v in json.load(json_file).items()}

    return d
