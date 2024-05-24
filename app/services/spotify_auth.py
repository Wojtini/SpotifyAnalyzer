import json
import os
import base64
from dotenv import load_dotenv
from requests import post

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

def get_token():
    if not client_id or not client_secret:
        raise ValueError("Brakujące CLIENT_ID lub CLIENT_SECRET w zmiennych środowiskowych")

    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}
    response = post(url, headers=headers, data=data)
    if response.status_code != 200:
        raise Exception(f"Nie udało się uzyskać tokenu, status code: {response.status_code}, odpowiedź: {response.text}")
    json_response = response.json()
    token = json_response.get("access_token")
    if not token:
        raise Exception("Nie udało się uzyskać tokenu z odpowiedzi")
    return token


def get_auth_header(token):
    return {"Authorization": "Bearer " + token}



