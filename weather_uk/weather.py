#!/usr/bin/env python2
"""
Get weather script
------------------
Usage: ./weather.py London
"""

import urllib2
import sys
import re

# https://apidev.accuweather.com/developers/countries
COUNTRY_CODE = "EUR|UK|UK150|"
UNITS = 1  # 0 for F, 1 for C
ACCUWEATHER_URL = ("http://rss.accuweather.com/rss/liveweather_rss.asp?metric="
                   "{units}&locCode={{location}}".format(units=UNITS))


def get_weather(location):
    url = ACCUWEATHER_URL.format(location=location)

    try:
        data = urllib2.urlopen(url).read()
    except Exception as error:
        print("Error occured: %s" % error)
        sys.exit(1)

    match_obj = re.search(r"<title>Currently\:\s(.+)</title>", data)

    if match_obj:
        return match_obj.group(1)
    else:
        print("Error parsing data...check name of Town/City")
        sys.exit(1)


def main():
    if len(sys.argv) != 2:
        print(__doc__.strip())
        sys.exit(1)

    town_city = sys.argv[1].strip().replace(' ', '')
    weather = get_weather(COUNTRY_CODE+town_city)
    print(weather)


if __name__ == "__main__":
    main()
