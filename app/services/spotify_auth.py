import base64
import os

from dotenv import load_dotenv
from requests import post

from app.exceptions.spotify_exceptions import (
    EnvironmentalVariableDoesNotExistError,
    SpotifyAuthError,
)

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
HTTP_OK_STATUS_CODE = 200
TIMEOUT = 10


def get_token() -> str:
    if not client_id or not client_secret:
        error_message = "Can't find proper environmental variables"
        raise EnvironmentalVariableDoesNotExistError(error_message)

    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded",
    }
    data = {"grant_type": "client_credentials"}
    response = post(url, headers=headers, data=data, timeout=TIMEOUT)
    if response.status_code != HTTP_OK_STATUS_CODE:
        error_message = (f"Error during receiving token: {response.status_code},"
                         f" message: {response.text}")
        raise SpotifyAuthError(error_message)
    json_response = response.json()
    return json_response.get("access_token")


def get_auth_header(token: str) -> dict[str, str]:
    return {"Authorization": "Bearer " + token}
