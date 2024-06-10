import base64
import random
import string
import urllib.parse

from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse, RedirectResponse
from pydantic import BaseModel
from requests import get, post

#token = 'BQCmOQQzlfC6Ghq70gUDXeoONtgxHkMEBhsJX5jrQUj_XE6_IgOQlIhCf79HU-XU_KFWcqNbKxha7u20PFm_wVm0VV65Cxquokdl_eFUbE5DuczfHmNEz2KQx62-f0X36kH3la1L6WTEkJ8tavVSd1s9A4gT9HQ3_z5qyKXdwXhn2jSHCAbDuBT_huLWX89oCIJa_nP60fCT3eDhb0bWTQEZAngmawyHfOfAJlxIAMoO2MXIgaaKgoBU49TGeLwozfB_SHh8stov0kEj'

router = APIRouter()
url = "https://api.spotify.com"
response_ok = 200
response_created = 201

CLIENT_ID = "0405fc9457ac42e3827b65fa40636571"
CLIENT_SECRET = "1d734c8dcc564c3cac7deb6349d634d9"
REDIRECT_URI = "http://localhost:8000/token_callback"
SCOPE = ",".join([
    "user-read-private",
    "user-read-email",
    "playlist-modify-public",
    "playlist-modify-private",
])

@router.get("/")
def login(request: Request):
    query_params = {
        "response_type": "code",
        "client_id": CLIENT_ID,
        "scope": SCOPE,
        "redirect_uri": REDIRECT_URI
    }

    url = "https://accounts.spotify.com/authorize?" + urllib.parse.urlencode(query_params)
    return RedirectResponse(url)


@router.get("/token_callback")
def callback(request: Request):
    code = request.query_params.get("code")

    auth_options = {
        "url": "https://accounts.spotify.com/api/token",
        "data": {
            "code": code,
            "redirect_uri": REDIRECT_URI,
            "grant_type": "authorization_code",
        },
        "headers": {
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": "Basic " + base64.b64encode(
                f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode(),
        },
    }
    response = post(auth_options["url"], data=auth_options["data"], headers=auth_options["headers"], timeout=30)
        
    if response.status_code == response_ok:
        token_info = response.json()
        return JSONResponse(token_info)
    else:
         return JSONResponse({"error": response.reason}, status_code=response.status_code)


class PlaylistRequest(BaseModel):
    token: str
    name: str = "New Playlist"
    description: str = "My new playlist"
    public: bool = True
    collaborative: bool = False

class Owner(BaseModel):
    href: str
    id: str
    type: str
    uri: str
    display_name: str
    external_urls: dict

class PlaylistResponse(BaseModel):
    name: str
    description: str
    owner: Owner



@router.post("/create_playlist")
def create_playlist(request_body: PlaylistRequest)-> PlaylistResponse:
    headers = {
        "Authorization": f"Bearer {request_body.token}",
    }
    user_profile_url = "https://api.spotify.com/v1/me"
    profile_response = get(user_profile_url, headers=headers, timeout=30)
    
    if profile_response.status_code != response_ok:
        raise HTTPException(status_code=profile_response.status_code, detail=profile_response.text)

    user_id = profile_response.json()["id"]
    create_playlist_url = f"https://api.spotify.com/v1/users/{user_id}/playlists"
    payload = {
        "name": request_body.name,
        "description": request_body.description,
        "public": request_body.public,
        "collaborative": request_body.collaborative,
    }
    playlist_response = post(create_playlist_url, json=payload, headers=headers, timeout=30)
    
    if playlist_response.status_code == response_created:
        return PlaylistResponse(playlist_response.json())
    else:
        raise HTTPException(status_code=playlist_response.status_code, detail="Failed to create playlist")