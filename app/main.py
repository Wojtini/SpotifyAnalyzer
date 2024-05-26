from fastapi import FastAPI

from app.routers.recommendations import api

app = FastAPI()
app.include_router(api)
