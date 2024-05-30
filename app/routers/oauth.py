import base64
import random
import string
import urllib.parse

from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.security import OAuth2PasswordBearer
from requests import get, post

router = APIRouter()
url = "https://api.spotify.com"

CLIENT_ID = "0405fc9457ac42e3827b65fa40636571"
CLIENT_SECRET = "1d734c8dcc564c3cac7deb6349d634d9"
REDIRECT_URI =  "http://localhost:8000/token_callback"
SCOPE = "user-read-private user-read-email"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token_callback")

def generate_random_string(length):
    return "".join(random.choices(string.ascii_letters + string.digits, k=length))

STATE = generate_random_string(16)

@router.get("/")
def login(request: Request):
    query_params = {
        "response_type": "code",
        "client_id": CLIENT_ID,
        "scope":  SCOPE,
        "redirect_uri": REDIRECT_URI,
        "state": STATE,
    }

    url = "https://accounts.spotify.com/authorize?" + urllib.parse.urlencode(query_params)
    return RedirectResponse(url)

@router.get("/token_callback")
def callback(request: Request):
    code = request.query_params.get("code")
    STATE =  request.query_params.get("state")

    if STATE is None:
        return RedirectResponse("/#" + urllib.parse.urlencode({"error": "state_mismatch"}))
    else:
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
        response = post(auth_options["url"],
                        data = auth_options["data"],
                        headers = auth_options["headers"])
    if response.status_code == 200:
        token_info = response.json()
        return JSONResponse(token_info)
    else:
        return JSONResponse({"error": response.reason}, status_code = response.status_code)


@router.post("/create_playlist")
def create_playlist(
        token: str =  Depends(oauth2_scheme),
        name: str = "New Playlist",
        description: str = "My new playlist",
        public: bool = True,
        collaborative: bool = False,
):
    user_profile_url = "https://api.spotify.com/v1/me"
    headers = {
        "Authorization": f"Bearer {token}",
    }
    profile_response = get(user_profile_url, headers = headers)
    if profile_response.status_code != 200:
        return JSONResponse({"error": "Failed to get user profile"}, status_code=profile_response.status_code)

    user_id = profile_response.json()["id"]
    create_playlist_url = f"https://api.spotify.com/v1/users/{user_id}/playlists"
    payload = {
          "name": name,
        "description": description,
        "public": public,
        "collaborative": collaborative,
    }
    playlist_response = post(create_playlist_url, json=payload, headers=headers)
    if playlist_response.status_code == 201:
        return JSONResponse(playlist_response.json())
    else:
        return JSONResponse({"error": "Failed to create playlist"}, status_code=playlist_response.status_code)
