from fastapi import FastAPI

from app.routers.auth import router as auth_api
from app.routers.songs import router as songs_router

app = FastAPI()

app.include_router(songs_router)
app.include_router(auth_api)
