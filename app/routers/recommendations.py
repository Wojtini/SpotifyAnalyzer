from fastapi import APIRouter,FastAPI,HTTPException
from app.models.requests import SpotifyRequest
from app.services.spotify_data_fetcher import get_spotify_recommendations_by_song
import requests

api = APIRouter()

@api.get("/v1/recommendations-by-song")
def get_recommendations_by_song(item: SpotifyRequest):
    return get_spotify_recommendations_by_song(item.name)
