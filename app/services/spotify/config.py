REQUEST_TIMEOUT = 10
REDIRECT_URI = "http://localhost:8000/auth/token_callback"

SCOPE = ",".join(  # noqa: FLY002
    [
        "playlist-modify-public",
        "playlist-modify-private",
    ],
)
