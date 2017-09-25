import json
import re
import requests

import api_key

API_KEY = api_key.API_KEY


def make_request(url, api_key=API_KEY, headers=dict()):
    """
    Make a request to the Riot API. This function will include the api key in the header, so no need to add the
    API key to the URL.
    """
    header_dict = headers
    # add api_key to the header
    header_dict.update({'X-Riot-Token': api_key})
    # return the response object
    return requests.get(url, headers=header_dict)


SUMMONER_NAME_RE = re.compile('^[0-9a-zA-Z _\\.]+$')
def validate_summoner_name(summoner_name):
    """
    Returns True if the summoner name complies with Riot's API requirements.
    https://developer.riotgames.com/getting-started.html
    I've made my regex more stringent than Riot's standards because the "\p{L}" expression doesn't seem to work
    with the "re" library.

    Looks to make sure all characters are alphanumeric or "_", " ", or "."
    """
    return SUMMONER_NAME_RE.search(summoner_name) is not None


def handle_response_error(response):
    response_dict = json.loads(response.text)
    status_code = response_dict['status']['status_code']
    message = response_dict['status']['message']
    print('{status_code}: {message}'.format(status_code=status_code, message=message))
