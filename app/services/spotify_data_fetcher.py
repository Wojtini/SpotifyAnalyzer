import json
from http.client import HTTPException

import requests
from app.services.spotify_auth import get_auth_header, get_token

url = "https://api.spotify.com/v1/search"

token = get_token()
headers = get_auth_header(token)


def fetch_data_from_spotify_by_query(song_name):
    query = f"?q={song_name}&type=track&limit=1"
    url_with_parameters = url + query

    response = requests.get(url_with_parameters, headers=headers)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code,
                            detail=f"Error fetching data from Spotify: {response.text}")

    json_response = response.json()
    return json_response
