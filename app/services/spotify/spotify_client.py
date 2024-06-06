import os
from base64 import b64encode
from functools import cached_property
from typing import Any

import requests

from app.services.spotify.config import REQUEST_TIMEOUT
from app.services.spotify.exceptions import (
    EnvironmentalVariableDoesNotExistError,
    SpotifyAuthError,
    SpotifyFetchError,
)
from app.services.spotify.models.song import Song

HTTP_OK_STATUS = 200


class SpotifyClient:
    def __init__(self) -> None:
        self.client_id = self._get_env_var("CLIENT_ID")
        self.client_secret = self._get_env_var("CLIENT_SECRET")

    def get_recommendations(self, songs_seed: list[Song], limit: int = 10) -> list[Song]:
        url = "https://api.spotify.com/v1/recommendations"
        seed_tracks = [song.id for song in songs_seed]
        seed_artists = [
            artist.id
            for song in songs_seed
            for artist in song.artists
        ]
        parameters = (
            f"?seed_tracks={','.join(seed_tracks)}"
            f"&seed_artists={','.join(seed_artists)}"
            f"&limit={limit}"
        )
        url_with_parameters = url + parameters
        response = self.get(url_with_parameters).json()
        return [Song(**track_dict) for track_dict in response["tracks"]]

    def search_for_song(self, query: str) -> Song:
        results = self.search_spotify(query, "track", 1)

        song_dict = results["tracks"]["items"][0]
        return Song(**song_dict)

    def search_spotify(self, query: str, search_type: str, limit: int = 1) -> dict:
        url = "https://api.spotify.com/v1/search"
        query = f"?q={query}&type={search_type}&limit={limit}"
        url_with_params = url + query

        response = self.get(url_with_params)
        if response.status_code != HTTP_OK_STATUS:
            raise SpotifyFetchError(response)

        return response.json()

    def get_auth_header(self) -> dict[str, str]:
        return {"Authorization": f"Bearer {self._token}"}

    @cached_property
    def _token(self) -> str:
        response = self.post(
            url="https://accounts.spotify.com/api/token",
            headers={
                "Authorization": "Basic " + self._auth_base64,
                "Content-Type": "application/x-www-form-urlencoded",
            },
            data={"grant_type": "client_credentials"},
        )
        if response.status_code != HTTP_OK_STATUS:
            raise SpotifyAuthError(response)
        return response.json().get("access_token")

    @property
    def _auth_base64(self) -> str:
        auth_bytes = self._auth_string.encode("utf-8")
        return str(b64encode(auth_bytes), "utf-8")

    @property
    def _auth_string(self) -> str:
        return f"{self.client_id}:{self.client_secret}"

    def get(self, url: str) -> requests.Response:
        return requests.get(url, headers=self.get_auth_header(), timeout=REQUEST_TIMEOUT)

    def post(self, url: str, *args: Any, **kwargs: Any) -> requests.Response:  # noqa: ANN401
        return requests.post(url, *args, **kwargs, timeout=REQUEST_TIMEOUT)

    @staticmethod
    def _get_env_var(var_name: str) -> str:
        env_var = os.getenv(var_name)
        if not env_var:
            raise EnvironmentalVariableDoesNotExistError(var_name)
        return env_var


SPOTIFY_CLIENT = SpotifyClient()


def get_spotify_client() -> SpotifyClient:
    return SPOTIFY_CLIENT
