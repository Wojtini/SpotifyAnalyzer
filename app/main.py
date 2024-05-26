from fastapi import FastAPI

from app.routers.hello_world import router as hello_world_router

<<<<<<< HEAD

=======
>>>>>>> 83db2983746822ff757f30bdeb7a4d0434944290
app = FastAPI()

app.include_router(hello_world_router)
