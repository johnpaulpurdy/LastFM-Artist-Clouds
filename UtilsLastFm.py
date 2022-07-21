import json
import requests
import requests_cache

requests_cache.install_cache()
USER_AGENT = os.environ['UserAgent']
fetch_limit = 5

def lastfm_get(payload):
    #define headers and URL
    headers = { 'user-agent': USER_AGENT}
    url = 'https://ws.audioscrobbler.com/2.0/'

    # Add API key and format to the payload
    payload['api_key'] = os.environ['lastFMApiKey']
    payload['format'] = 'json'
    response = requests.get(url, headers=headers, params=payload )
    return response