from typing import Annotated

from fastapi import APIRouter, Depends

from app.services.spotify.models.song import Song
from app.services.spotify.spotify_client import SpotifyClient, get_spotify_client

api = APIRouter(prefix="/v1", tags=["v1"])


@api.get("/recommendations")
def get_recommendations_by_song(
    query: str,
    spotify_client: Annotated[SpotifyClient, Depends(get_spotify_client)],
) -> list[Song]:
    song = spotify_client.search_for_song(query)
    return spotify_client.get_recommendations([song])


@api.get("/song")
def get_song(
    query: str,
    spotify_client: Annotated[SpotifyClient, Depends(get_spotify_client)],
) -> Song:
    return spotify_client.search_for_song(query)
