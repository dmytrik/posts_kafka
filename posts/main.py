import logging
from fastapi import FastAPI
from contextlib import asynccontextmanager
from routes import router
from producer import init_kafka_producer, shutdown_kafka_producer


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_kafka_producer()
    try:
        yield
    finally:
        await shutdown_kafka_producer()


app = FastAPI(lifespan=lifespan)

app.include_router(router, prefix="/api/v1/posts", tags=["posts"])
