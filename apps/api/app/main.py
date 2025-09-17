from fastapi import FastAPI
from .api.v1.chats import router as chats_router

app = FastAPI()

# Include API routers
app.include_router(chats_router, prefix="/api", tags=["chats"])


@app.get("/")
def read_root():
    return {"Hello": "World"}
