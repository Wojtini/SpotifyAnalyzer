import json
import requests
from http.client import HTTPException
from app.models.responses import RecommendationResponse, Page
from app.services.spotify_auth import get_auth_header, get_token

token = get_token()
headers = get_auth_header(token)
SEARCH_URL = "https://api.spotify.com/v1/search"
RECOMMENDATIONS_URL = "https://api.spotify.com/v1/recommendations"


def get_spotify_recommendations_by_song(song_name):
    search_response_json = get_json_of_spotify_search_request(song_name, "track")
    seed_tracks = get_track_seed_from_search_response(search_response_json)
    seed_artist = get_artist_seed_from_search_response(search_response_json)
    recommendations_json = get_recommendations_response_json(seed_tracks, seed_artist)
    return map_to_page_of_recommendation_response(recommendations_json)


def get_json_of_spotify_search_request(unit_to_search_by, type_of_unit):
    query = f"?q={unit_to_search_by}&type={type_of_unit}&limit=1"
    url_with_parameters = SEARCH_URL + query

    response = requests.get(url_with_parameters, headers=headers)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code,
                            detail=f"Error fetching data from Spotify: {response.text}")

    return response.json()


def get_track_seed_from_search_response(json_response):
    track_id = json_response["tracks"]["items"][0]["id"]
    return track_id


def get_artist_seed_from_search_response(json_response):
    main_artist_id = json_response["tracks"]["items"][0]["artists"][0]["id"]
    return main_artist_id


def get_recommendations_response_json(seed_tracks, seed_artist):
    parameters = f"?seed_tracks={seed_tracks}&seed_artist={seed_artist}&limit=10"
    url_with_parameters = RECOMMENDATIONS_URL + parameters
    response = requests.get(url_with_parameters, headers=headers)
    return response.json()


def map_to_page_of_recommendation_response(recommendation_json):
    recommendation_items = []
    for track in recommendation_json["tracks"]:
        recommendation_items.append(
            RecommendationResponse(artist_name=track["artists"][0]['name'], song_name=track['name']))
    page = Page(items=recommendation_items, page_number=1, page_size=10, total_items=10)
    return page
