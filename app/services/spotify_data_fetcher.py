from services.spotify_auth import get_auth_header, get_token

url = "https://accounts.spotify.com/v1/search"


token = get_token()

header = get_auth_header(token)
def fetch_data_from_spotify_by_query(song_name):
    body = {
        "q": song_name,
        "limit": 10,
        "type": "track"
    }











