from http.client import HTTPException
from typing import Any

import requests

from app.models.responses import Page, RecommendationResponse
from app.services.spotify_auth import get_auth_header, get_token

token = get_token()
headers = get_auth_header(token)
SEARCH_URL = "https://api.spotify.com/v1/search"
RECOMMENDATIONS_URL = "https://api.spotify.com/v1/recommendations"
TIMEOUT = 20
HTTP_STATUS_OK_CODE = 200


def get_spotify_recommendations_by_song(song_name: str) -> Page:
    search_response_json = get_json_of_spotify_search_request(song_name, "track")
    seed_tracks = get_track_seed_from_search_response(search_response_json)
    seed_artist = get_artist_seed_from_search_response(search_response_json)
    recommendations_json = get_recommendations_response_json(seed_tracks, seed_artist)
    return map_to_page_of_recommendation_response(recommendations_json)


def get_json_of_spotify_search_request(unit_to_search_by: str, type_of_unit: str) -> dict[str, Any]:
    query = f"?q={unit_to_search_by}&type={type_of_unit}&limit=1"
    url_with_parameters = SEARCH_URL + query

    response = requests.get(url_with_parameters, headers=headers, timeout=TIMEOUT)

    if response.status_code != HTTP_STATUS_OK_CODE:
        error_message = f"Error fetching data from Spotify: {response.text}"
        raise HTTPException(error_message)

    return response.json()


def get_track_seed_from_search_response(json_response: dict[str, Any]) -> str:
    return json_response["tracks"]["items"][0]["id"]


def get_artist_seed_from_search_response(json_response: dict[str, Any]) -> str:
    return json_response["tracks"]["items"][0]["artists"][0]["id"]


def get_recommendations_response_json(seed_tracks: str, seed_artist: str) -> dict[str, Any]:
    parameters = f"?seed_tracks={seed_tracks}&seed_artists={seed_artist}&limit=10"
    url_with_parameters = RECOMMENDATIONS_URL + parameters
    response = requests.get(url_with_parameters, headers=headers, timeout=TIMEOUT)
    return response.json()


def map_to_page_of_recommendation_response(recommendation_json: dict[str, Any]) -> Page:
    recommendation_items = [
        RecommendationResponse(artist_name=track["artists"][0]["name"], song_name=track["name"])
        for track in recommendation_json["tracks"]
    ]
    return Page(items=recommendation_items, page_number=1, page_size=10, total_items=10)
