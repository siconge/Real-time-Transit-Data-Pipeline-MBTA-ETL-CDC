from threading import Timer
from datetime import datetime
import time
import json, ssl
import urllib.request, urllib.error
from cdc.mysql_db import insert_mbta_record

from utils.constants import MBTA_API_URL

ssl._create_default_https_context = ssl._create_unverified_context

timeout_seconds = 30

# Extract records with all required fields from the parsed JSON returned by calling the MBTA API; insert the record list into MySQL database
def call_mbta_api():
    mbta_dict_list = []
    with urllib.request.urlopen(MBTA_API_URL, timeout=timeout_seconds) as url:
        data = json.loads(url.read().decode())
        for bus in data['data']:
            bus_dict = dict()
            bus_dict['id'] = bus['id']
            bus_dict['bearing'] = bus['attributes']['bearing']
            bus_dict['current_status'] = bus['attributes']['current_status']
            bus_dict['current_stop_sequence'] = bus['attributes']['current_stop_sequence']
            bus_dict['direction_id'] = bus['attributes']['direction_id']
            bus_dict['longitude'] = bus['attributes']['longitude']
            bus_dict['latitude'] = bus['attributes']['latitude']
            updated_at_str = bus['attributes']['updated_at']
            updated_at_dt = datetime.fromisoformat(updated_at_str)
            bus_dict['updated_at'] = updated_at_dt.strftime('%Y-%m-%d %H:%M:%S')
            mbta_dict_list.append(bus_dict)
    insert_mbta_record(mbta_dict_list)
    return mbta_dict_list

# Periodically call the MBTA API and process data
def mbta_api_timeloop():
    '''
    This function continuously calls the MBTA API every 10 seconds.
    If an error occurs during the API call, it will retry after a delay.
    The retrieved data is processed and inserted into the MySQL database.
    '''
    print(f'--- ' + time.ctime() + ' ---')
    try:
        call_mbta_api()
    except urllib.error.URLError as e:
        if isinstance(e.reason, TimeoutError):
            print("Timeout error. Retrying in 10 seconds...")
            Timer(10, mbta_api_timeloop).start()
        else:
            print("Unexpected error:", e)
    else:
        Timer(10, mbta_api_timeloop).start()