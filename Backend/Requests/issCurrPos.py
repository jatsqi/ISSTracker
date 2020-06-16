import requests
from datetime import datetime
from Backend.Core.database import redisDB

# ISS current location API URL
ISS_LOCATION_URL = 'http://api.open-notify.org/iss-now.json'


def currPos():

    # Get request to get the current position of ISS from 'http://api.open-notify.org/iss-now.json'
    response = requests.get(ISS_LOCATION_URL)
    status = response.status_code

    # If an API call was not successful raise an exception.
    if status != 200:
        raise Exception ("ISS API unreachable.")
    else:
        data = response.json()

        # Read data from response
        latitude = data['iss_position']['latitude']
        longitude = data['iss_position']['longitude']
        timestamp = data['timestamp']

        # Convert timestamp to datetime and format datetime;
        # The timestamp comes as a UNIX-Timestamp which is defined as
        # "the number of seconds (or milliseconds) elapsed since an absolute point in time,
        # midnight of Jan 1 1970 in UTC time."
        dt_obj = datetime.fromtimestamp(timestamp).strftime(format="%Y-%m-%d %H-%M-%S")

        # Create a dictionary with the values latitude, longitude, timestamp and return data in dictionary
        iss_dict = {'latitude': float(latitude), 'longitude': float(longitude), 'timestamp': dt_obj}

        # Push data to DB
        redisDB().setData(data=iss_dict, requestname='ISSpos')

        return iss_dict
