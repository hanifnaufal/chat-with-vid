from fastapi import FastAPI, Request
from .api.v1 import chats as chats_router
from .core.logging import setup_logging
import time

# Set up logging
logger = setup_logging()

app = FastAPI()

# Include API routers
app.include_router(chats_router.router, prefix="/api/v1", tags=["chats"])


# Middleware for request logging
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()

    # Process request
    response = await call_next(request)

    # Log request details
    process_time = time.time() - start_time
    logger.info(
        "Request processed",
        extra={
            "url": str(request.url),
            "method": request.method,
            "status_code": response.status_code,
            "process_time": f"{process_time:.4f}s",
        },
    )

    return response


@app.get("/")
def read_root():
    logger.info("Root endpoint accessed")
    return {"Hello": "World"}
