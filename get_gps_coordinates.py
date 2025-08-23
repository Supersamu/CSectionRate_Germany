from geopy.geocoders import Nominatim
import json
import logging
import time

def get_cache_key(clinic_data):
    # transform the clinic_data dictionary into a string representation
    clinic_data_str = json.dumps(clinic_data, sort_keys=True)
    return clinic_data_str

def get_coordinates_from_clinic_data(clinic_data, cache_file='coordinates_cache.json'):
    # Load cache if exists
    try:
        with open(cache_file, 'r') as f:
            cache = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        cache = {}

    key = get_cache_key(clinic_data)
    if key in cache:
        return tuple(cache[key])

    geolocator = Nominatim(user_agent="csection_rate_analysis")
    location = geolocator.geocode(query=clinic_data, country_codes='de')
    time.sleep(2)  # maximum of 1 request per second according to Terms of Use
    if location:
        coords = (location.latitude, location.longitude)
        cache[key] = coords
        with open(cache_file, 'w') as f:
            json.dump(cache, f)
        return coords
    # log the cases where location is not found
    logging.warning(f"Location not found for: {clinic_data}")
    return None