from fastapi import FastAPI
from .api.v1 import chats as chats_router

app = FastAPI()

# Include API routers
app.include_router(chats_router.router, prefix="/api/v1", tags=["chats"])


@app.get("/")
def read_root():
    return {"Hello": "World"}
