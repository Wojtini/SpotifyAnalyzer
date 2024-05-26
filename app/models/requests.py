from pydantic import BaseModel

class SpotifyRequest(BaseModel):
    name: str

