import base64
import random
import string
import urllib.parse

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse, RedirectResponse
from requests import post

router = APIRouter()
url = "https://api.spotify.com"

CLIENT_ID = "0405fc9457ac42e3827b65fa40636571"
CLIENT_SECRET = "1d734c8dcc564c3cac7deb6349d634d9"
REDIRECT_URI =  "http://localhost:8000/token_callback"
SCOPE = "user-read-private user-read-email"

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
                "Authorization": "Basic " + base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode(),
            },
        }

        response = post(auth_options["url"], data = auth_options["data"], headers = auth_options["headers"])
    if response.status_code == 200:
        token_info = response.json()
        return JSONResponse(token_info)
    else:
        return JSONResponse({"error": response.reason}, status_code = response.status_code)


