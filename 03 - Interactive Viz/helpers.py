"""Helpers for Homework 03 of ADA"""

import re
import json
import requests
import googlemaps

def get_canton(university_name, swiss_cantons):
    """Get the swiss canton of a university, given a name and the list
    of valid cantons codes.
    
    The canton is retrieved following this method :
    1. First we try to match a swiss canton code in the name string, ie. a
       two-letter code located at the end of the string.
    2. If no code is found in step 1, we use the Google Places
       geocoding API.

    If no canton code is found, return None.
    """

    # First try to extract canton code from name string
    canton_regex = r"-\s*([A-Z]{2})$" # matches 2-letter codes at the end
    regex_obj = re.compile(canton_regex)
    codes = regex_obj.findall(university_name)
    if len(codes) != 0:
        if codes[0] in swiss_cantons:
            return codes[0]

    # No code found : try to retrieve info using Google Places geocoding API
    name_split = university_name.split('-')[0].strip() # omit abbreviations
    with open('api-key.txt', 'r') as api_file:
        api_key = api_file.read().replace('\n', '') # api key for Google API

    gmaps = googlemaps.Client(key=api_key)
    geocode_result = gmaps.geocode(name_split)
    if len(geocode_result) != 0:
        result = geocode_result[0]
        
        for component in result['address_components']:
            types = component['types']
            if 'administrative_area_level_1' in types:
                code = component['short_name']
                if code in swiss_cantons:
                    return code

    return None
