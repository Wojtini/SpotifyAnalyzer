from http import HTTPStatus

from fastapi import HTTPException

from app.services.spotify.models.schemas import Playlist as PlaylistSchema
from app.services.spotify.models.schemas import Song
from app.services.spotify.models.user import User
from app.services.spotify.spotify_client import get_spotify_client


class Playlist:
    def __init__(
        self,
        owner: User,
        name: str,
        description: str = "",
        public: bool = False,
        collaborative: bool = False,
    ) -> None:
        self.client = get_spotify_client()
        self.create_playlist_url = f"https://api.spotify.com/v1/users/{owner.user_id}/playlists"
        payload = {
            "name": name,
            "description": description,
            "public": public,
            "collaborative": collaborative,
        }
        response = self.client.post(
            self.create_playlist_url,
            json=payload,
            headers=owner.auth_header,
        )
        response_json = response.json()
        if response.status_code != HTTPStatus.CREATED:
            raise HTTPException(
                status_code=response.status_code,
                detail=response.content,
            )
        self.owner = owner
        self.name = response_json["name"]
        self.description = response_json["description"]
        self.public = response_json["public"]
        self.collaborative = response_json["collaborative"]
        self.playlist_id = response_json["id"]

    def add_songs(self, songs: list[Song]) -> None:
        client = get_spotify_client()
        uris = ",".join([song.uri for song in songs])
        response = client.post(
            url=f"https://api.spotify.com/v1/playlists/{self.playlist_id}/tracks?uris={uris}",
            headers=self.owner.auth_header,
        )
        if response.status_code not in (HTTPStatus.CREATED, HTTPStatus.OK):
            raise HTTPException(
                status_code=response.status_code,
                detail=response.content,
            )

    def fetch_model(self) -> PlaylistSchema:
        playlist_url = f"https://api.spotify.com/v1/playlists/{self.playlist_id}"
        response = self.client.get(url=playlist_url, headers=self.owner.auth_header)
        response_json = response.json()
        playlist_songs = [song["track"] for song in response_json["tracks"]["items"]]
        response_json.update({"songs": playlist_songs})
        return PlaylistSchema.model_validate(response_json)
