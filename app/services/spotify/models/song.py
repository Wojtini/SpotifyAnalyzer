from pydantic import BaseModel

from app.services.spotify.models.artist import Artist


class Song(BaseModel):
    id: str
    name: str
    artists: list[Artist]
