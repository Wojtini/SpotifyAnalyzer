import os
from base64 import b64encode
from functools import cached_property
from http import HTTPStatus
from typing import Any

import requests
from fastapi import HTTPException
from requests import PreparedRequest

from app.services.spotify.config import REDIRECT_URI, REQUEST_TIMEOUT, SCOPE
from app.services.spotify.models.schemas import Song, SpotifyToken


class SpotifyClient:
    def __init__(self) -> None:
        self.client_id = self._get_env_var("CLIENT_ID")
        self.client_secret = self._get_env_var("CLIENT_SECRET")

    def get_recommendations(self, songs_seed: list[Song], limit: int = 10) -> list[Song]:
        url = "https://api.spotify.com/v1/recommendations"
        seed_tracks = [song.id for song in songs_seed]
        seed_artists = [artist.id for song in songs_seed for artist in song.artists]
        parameters = (
            f"?seed_tracks={','.join(seed_tracks)}"
            f"&seed_artists={','.join(seed_artists)}"
            f"&limit={limit}"
        )
        url_with_parameters = url + parameters
        response = self.get(
            url=url_with_parameters,
            headers=self._get_auth_header(),
        ).json()
        return [Song(**track_dict) for track_dict in response["tracks"]]

    def search_for_song(self, query: str) -> Song:
        results = self.search_spotify(query, "track", 1)

        song_dict = results["tracks"]["items"][0]
        return Song(**song_dict)

    def search_spotify(self, query: str, search_type: str, limit: int = 1) -> dict:
        url = "https://api.spotify.com/v1/search"
        query = f"?q={query}&type={search_type}&limit={limit}"
        url_with_params = url + query

        response = self.get(
            url_with_params,
            headers=self._get_auth_header(),
        )
        if response.status_code != HTTPStatus.OK:
            raise HTTPException(
                status_code=response.status_code,
                detail=response.content,
            )

        return response.json()

    def get_oauth_url(self) -> str:
        url = "https://accounts.spotify.com/authorize"
        params = {
            "response_type": "code",
            "client_id": self.client_id,
            "scope": SCOPE,
            "redirect_uri": REDIRECT_URI,
        }
        req = PreparedRequest()
        req.prepare_url(url, params)
        if not req.url:
            raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR)
        return req.url

    def swap_code_to_token(self, code: str) -> SpotifyToken:
        response = self.post(
            url="https://accounts.spotify.com/api/token",
            data={
                "code": code,
                "redirect_uri": REDIRECT_URI,
                "grant_type": "authorization_code",
            },
            headers={
                "Content-Type": "application/x-www-form-urlencoded",
                "Authorization": "Basic " + self._auth_base64,
            },
        ).json()
        return SpotifyToken(**response)

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
        if response.status_code != HTTPStatus.OK:
            raise HTTPException(
                status_code=response.status_code,
                detail=response.content,
            )
        return response.json()["access_token"]

    @property
    def _auth_base64(self) -> str:
        auth_bytes = self._auth_string.encode("utf-8")
        return str(b64encode(auth_bytes), "utf-8")

    @property
    def _auth_string(self) -> str:
        return f"{self.client_id}:{self.client_secret}"

    def get(self, url: str, *args: Any, **kwargs: Any) -> requests.Response:  # noqa: ANN401
        return requests.get(url, *args, **kwargs, timeout=REQUEST_TIMEOUT)

    def post(self, url: str, *args: Any, **kwargs: Any) -> requests.Response:  # noqa: ANN401
        return requests.post(url, *args, **kwargs, timeout=REQUEST_TIMEOUT)

    def _get_auth_header(self) -> dict[str, str]:
        return {"Authorization": f"Bearer {self._token}"}

    @staticmethod
    def _get_env_var(var_name: str) -> str:
        env_var = os.getenv(var_name)
        if not env_var:
            msg = "Credentials not found in environment variables"
            raise ValueError(msg)
        return env_var


SPOTIFY_CLIENT = SpotifyClient()


def get_spotify_client() -> SpotifyClient:
    return SPOTIFY_CLIENT
