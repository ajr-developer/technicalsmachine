#RestfulClient.py
#Referenced https://stackoverflow.com/a/32721995/6502196

import requests
import json

def get(url):
    """ Makes a GET request to the given RESTful API (no credentials)
    :param url: URL to call
    :type symbol: str.
    :returns: API response
    :type returns: JSON object
    
    """
    url = url
    myResponse = requests.get(url)

    # For successful API call, response code will be 200 (OK)
    if(myResponse.ok):

        # Loading the response data into a dict variable
        # json.loads takes in only binary or string variables so using content to fetch binary content
        # Loads (Load String) takes a Json file and converts into python data structure (dict or list, depending on JSON)
        jData = json.loads(myResponse.content)
        print(jData)
        return jData

    else:
    # If response code is not ok (200), print the resulting http error code with description
        myResponse.raise_for_status()
