from fastapi import APIRouter,FastAPI,HTTPException
from app.models.requests import Song
from app.services.spotify_data_fetcher import fetch_data_from_spotify_by_query
import requests

api = APIRouter()


@api.get("/v1/recommendations-by-song")
def get_recommendations_by_song(item: Song):
    return fetch_data_from_spotify_by_query(item.name)

