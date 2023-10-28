#!/usr/bin/env python3
"""Fetches metars from the ADDS Text Data Server.

Documentation: https://aviationweather.gov/dataserver

URL: https://aviationweather.gov/adds/dataserver_current/httpparam?datasource=metars&requestType=retrieve&format=xml&mostRecentForEachStation=constraint&hoursBeforeNow=1.5&stationString=CYEG

"""

__RCS__ = '$Id$'
__version__ = '$Revision:$'
__initialdate__ = 'August 2016'
__author__ = 'Darren Paul Griffith <https://madphilosopher.ca/>'


from xml.etree import ElementTree
import requests
import time
import random


DEBUG = False
TESTFILE = "cyeg.xml"
TESTFILE = "cyeg_cyoj.xml"

URL = 'https://aviationweather.gov/adds/dataserver_current/httpparam?datasource=metars&requestType=retrieve&format=xml&mostRecentForEachStation=constraint&hoursBeforeNow=1.5&stationString='


def degrees_to_cardinal(degrees):
    """Convert degrees >= 0 to one of 16 cardinal directions."""

    CARDINALS = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE", "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]
    degrees = float(degrees)
    if degrees < 0:
        return None

    i = (degrees + 11.25)/22.5
    return CARDINALS[int(i % 16)]


def fetch_multiple(station_list=list(["CYEG", "CYOJ"])):
    """Fetch the metars for a list of station IDs."""

    ''' convert list to space-separated string - use %20 as it will be used in a URL '''
    stations = "%20".join(station_list)
    if DEBUG:
        print("stations:", stations)

    ''' fetch the url and parse the xml data '''
    url = URL + stations
    tree = None
    if DEBUG:
        f = open(TESTFILE, 'rt')
        tree = ElementTree.parse(f)
    else:
        attempts = 0
        success = False
        while attempts < 3 and not success:
            try:
                rq = requests.get(url, timeout=16.0)
                rq.raise_for_status()
                if rq.status_code == requests.codes.ok:
                    intext = rq.text
                    tree = ElementTree.fromstring(intext)
                success = True
            except Exception as err:
                print(f"Unexpected {err=}, {type(err)=}")
                attempts = attempts + 1
                time.sleep(random.uniform(3,60))

    ''' start walking the tree '''
    out_dict = {}
    if tree:
        for node in tree.findall("./data/METAR"):
            s_metar = {}
            for x in node:
                ''' store each tag in a dictionary for that station '''
                s_metar[x.tag] = x.text
    
            ''' convert some keys '''
            if "wind_dir_degrees" in s_metar:
                s_metar["wind_dir_compass"] = degrees_to_cardinal(s_metar["wind_dir_degrees"])
            if "temp_c" in s_metar:
                s_metar["temp_f"] = float(s_metar["temp_c"])*9.0/5.0 + 32.0
            if "wind_speed_kt" in s_metar:
                s_metar["wind_speed_mph"] = float(s_metar["wind_speed_kt"]) * 1.150779
            if "sea_level_pressure_mb" in s_metar:
                s_metar["sea_level_pressure_kpa"] = float(s_metar["sea_level_pressure_mb"]) / 10.0
    
            ''' store the entire station metar dictionary in a dictionary '''
            out_dict[s_metar["station_id"]] = s_metar

    return out_dict


def fetch(station="CYEG"):
    """Fetch the metar for a single station ID."""

    d = fetch_multiple([station])
    return d.get(station) # returns None if d has no such key


if __name__ == '__main__':

    import sys

    if len(sys.argv) == 2:
        station = sys.argv[1].upper()
    else:
        station = "CYEG"
        station = "KATL"
        #station = "VABB"

    if DEBUG:
        import pprint
        pprint.pprint(fetch(station))
        print()

    d = fetch(station)
    if d:
        if DEBUG:
            print()
        print("Observation (UTC):        ", d["observation_time"] )
        print("Code:                     ", d["metar_type"] )
        print("Station:                  ", d["station_id"] )
        print("Raw Text:                 ", d["raw_text"] )
        print("Temperature (Celsius):    ", d["temp_c"] )
        print("Dew Point (Celsius):      ", d["dewpoint_c"] )
        print("Wind Speed (Kt):          ", d["wind_speed_kt"] )
        if "wind_gust_kt" in d:
            print("Wind Gust (Kt):           ", d["wind_gust_kt"] )
        print("Wind Direction Compass:   ", d["wind_dir_compass"] if "wind_dir_compass" in d else "" )
        print("Wind Direction (degrees): ", d["wind_dir_degrees"] if "wind_dir_degrees" in d else "" )
        print("Sea Level Pressure (Hpa): ", d["sea_level_pressure_mb"] if "sea_level_pressure_mb" in d else "")
        print("Sea Level Pressure (Kpa): ", d["sea_level_pressure_kpa"] if "sea_level_pressure_kpa" in d else "")


