from __future__ import annotations

from http import HTTPStatus

from fastapi import HTTPException

from app.services.spotify.spotify_client import get_spotify_client


class User:
    def __init__(
        self,
        token: str,
        user_id: str,
        display_name: str,
        href: str,
    ) -> None:
        self.user_id = user_id
        self.display_name = display_name
        self.href = href
        self.token = token

    @classmethod
    def from_token(cls, token: str) -> User:
        client = get_spotify_client()
        response = client.get(
            url="https://api.spotify.com/v1/me",
            headers={"Authorization": f"Bearer {token}"},
        )
        if response.status_code != HTTPStatus.OK:
            raise HTTPException(
                status_code=response.status_code,
                detail=response.content,
            )
        response_json = response.json()
        return cls(
            token=token,
            user_id=response_json["id"],
            display_name=response_json["display_name"],
            href=response_json["href"],
        )

    @property
    def auth_header(self) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {self.token}",
        }
