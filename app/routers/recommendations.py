from fastapi import APIRouter,FastAPI,HTTPException
from app.models.requests import Song
from app.services.spotify_auth import get_token
import requests

api = APIRouter()


@api.get("/v1/recommendations-by-song")
def get_recommendations_by_song(item: Song):
    token = get_token()
    return token

