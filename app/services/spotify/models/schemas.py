from pydantic import AliasChoices, BaseModel, Field


class SpotifyToken(BaseModel):
    access_token: str
    token_type: str
    expires_in: int
    refresh_token: str
    scope: str


class Artist(BaseModel):
    id: str
    name: str
    href: str


class Song(BaseModel):
    id: str
    name: str
    artists: list[Artist]
    uri: str


class User(BaseModel):
    user_id: str = Field(validation_alias=AliasChoices("id", "user_id"))
    display_name: str
    href: str

    class Config:
        from_attributes = True
