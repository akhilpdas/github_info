# common fucntions

import requests
from requests.auth import HTTPBasicAuth


AUTH_TOKEN = HTTPBasicAuth('gigahex-nsl','24a4943a813bef582759522d84925f90919d8c13')
BASE_URL = 'https://api.github.com/'


def github_get_operation(url, auth):
    """Getting data from github apis."""

    auth = HTTPBasicAuth('', auth)
    url = BASE_URL + url
    response = requests.get(url, auth=auth)
    response = response.json()
    return response