from pydantic import BaseModel

class Song(BaseModel):
    name: str


class SpotifyRequest(BaseModel):
    limit: int