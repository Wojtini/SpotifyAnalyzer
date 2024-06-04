from fastapi import APIRouter

from app.models.requests import SpotifyRequest
from app.models.responses import Page
from app.services.spotify_data_fetcher import get_spotify_recommendations_by_song

api = APIRouter()


@api.get("/v1/recommendations-by-song")
def get_recommendations_by_song(name: str) -> Page:
    return get_spotify_recommendations_by_song(name)
