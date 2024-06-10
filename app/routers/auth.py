from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.services.spotify.models.schemas import SpotifyToken
from app.services.spotify.models.schemas import User as UserSchema
from app.services.spotify.models.user import User
from app.services.spotify.spotify_client import SpotifyClient, get_spotify_client

router = APIRouter(prefix="/auth", tags=["auth"])

security = HTTPBearer()


@router.get("/token")
def init_token_exchange(
    spotify_client: Annotated[SpotifyClient, Depends(get_spotify_client)],
) -> RedirectResponse:
    return RedirectResponse(spotify_client.get_oauth_url())


@router.get("/token_callback", include_in_schema=False)
def callback(
    code: str,
    spotify_client: Annotated[SpotifyClient, Depends(get_spotify_client)],
) -> SpotifyToken:
    if not code:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="No code in callback found",
        )
    return spotify_client.swap_code_to_token(code)


@router.get("/me")
def me(
    token: Annotated[HTTPAuthorizationCredentials, Depends(security)],
) -> UserSchema:
    user = User.from_token(token.credentials)
    return UserSchema.model_validate(user)
