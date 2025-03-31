import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI

from consumer import (
    connect_kafka,
    consume,
    logger,
    consumer
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_kafka()
    task = asyncio.create_task(consume())
    try:
        await task
        logger.info("Kafka consumer task started")
    except asyncio.CancelledError:
        logger.info("Kafka consumer task cancelled")

    yield
    task.cancel()
    if consumer:
        await consumer.stop()
        logger.info("Kafka consumer stopped")


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def root():
    return {"message": "Notifications service is running"}
