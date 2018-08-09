# import libraries
import urllib.request
import urllib.error
import re
import time
from bs4 import BeautifulSoup


def get_data():
    storm_data = 'http://www.ssd.noaa.gov/PS/TROP/tdpositions.html#ATL'
    page = urllib.request.urlopen(storm_data)
    soup = BeautifulSoup(page, "html.parser")
    results = soup.div.pre.prettify()
    res_split = results.split('-->')
    raw_data = []

    # regex parses each piece of data for the db
    for x in res_split:
        # looks for... 14/1200 ...two digits and a forward slash, followed by four more digits
        date_time_u_t_c = re.search(r'(\d{2}\/\d{4})', x, flags=0)

        # looks for... 21.4N   109.4W' ...two sets of one-to-three digits, plus a decimal number, and is
        # paired with a letter and space between sets
        storm_loc = re.search(r'(\d{1,3}\.\d[A-Z]\s*\d{1,3}\.\d[A-Z])', x, flags=0)

        # looks for... T1.5/2.5 ...upper case T, two digits separated by decimal, a slash, and two more digits with dec
        storm_class = re.search(r'(T\d\.\d\/\d\.\d)', x, flags=0)

        # looks for... BUD ...a word beside two dashes
        storm_name = re.search(r'(\w*)(?=\s--)', x, flags=0)

        # looks for... East Pacific ...all content between <strong></strong> tags
        storm_region = re.search(r'(?<=<strong>)(.*)(?=<\/strong>)', x, flags=0)

        if date_time_u_t_c and storm_loc and storm_class and storm_name:
            storm_loc_split = storm_loc[1].split(" ")
            storm_lat = storm_loc_split[0]
            storm_long = storm_loc_split[0-1]
            timestamp = time.time()
            raw_data.append({'timestamp': timestamp, 'datetime': date_time_u_t_c[1], 'stormlat': storm_lat,
                                        'stormlong': storm_long, 'stormclass': storm_class[1],
                                        'stormname': storm_name[1], 'stormregion': storm_region[1]})

    return raw_data


def main(event, context):
    data = get_data()
    return data
