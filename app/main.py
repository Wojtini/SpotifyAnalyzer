import os

from fastapi import FastAPI

from app.routers.hello_world import router as hello_world_router
from app.routers.recommendations import api




app = FastAPI()
print(os.getenv("CLIENT_ID"))
app.include_router(api)
