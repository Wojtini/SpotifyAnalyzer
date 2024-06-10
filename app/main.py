from fastapi import FastAPI

from app.routers.oauth import router as oauth_router
from app.routers.recommendations import api

app = FastAPI()
app.include_router(api)
app.include_router(oauth_router)

app = FastAPI()
