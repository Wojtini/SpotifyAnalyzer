from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.services.spotify.models.playlist import Playlist
from app.services.spotify.models.schemas import Playlist as PlaylistSchema
from app.services.spotify.models.schemas import PlaylistCreate, Song
from app.services.spotify.models.user import User
from app.services.spotify.spotify_client import SpotifyClient, get_spotify_client

router = APIRouter(prefix="/v1", tags=["v1"])

security = HTTPBearer()


@router.post("/create_recommendations_playlist")
def create_playlist_from_recommendations(
    token: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    query: str,
    playlist_schema: PlaylistCreate,
    spotify_client: Annotated[SpotifyClient, Depends(get_spotify_client)],
    limit: int = 10,
) -> PlaylistSchema:
    user = User.from_token(token.credentials)
    song = spotify_client.search_for_song(query)
    recommendations = spotify_client.get_recommendations([song], limit)

    playlist = Playlist(
        owner=user,
        name=playlist_schema.name,
        description=playlist_schema.description,
        collaborative=playlist_schema.collaborative,
        public=playlist_schema.public,
    )
    playlist.add_songs(recommendations)
    return playlist.fetch_model()


@router.get("/recommendations")
def get_recommendations_by_song(
    query: str,
    spotify_client: Annotated[SpotifyClient, Depends(get_spotify_client)],
) -> list[Song]:
    song = spotify_client.search_for_song(query)
    return spotify_client.get_recommendations([song])


@router.get("/song")
def get_song(
    query: str,
    spotify_client: Annotated[SpotifyClient, Depends(get_spotify_client)],
) -> Song:
    return spotify_client.search_for_song(query)
