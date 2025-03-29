import asyncio
import json
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from aiokafka import AIOKafkaConsumer
from email_service import send_email


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def consume_kafka(app: FastAPI):

    consumer = None
    max_retries = 5
    retry_delay = 5

    for attempt in range(max_retries):
        try:
            logger.info(f"Connecting to Kafka... Attempt {attempt + 1}")
            consumer = AIOKafkaConsumer(
                "post_created",
                bootstrap_servers="kafka:9092",
                group_id="notification_group",
                auto_offset_reset="earliest"
            )
            await consumer.start()
            logger.info("Successfully connected to Kafka")
            break
        except Exception as e:
            logger.error(f"Attempt {attempt + 1} failed: {e}")
            if attempt < max_retries - 1:
                await asyncio.sleep(retry_delay)
            else:
                raise Exception("Failed to connect to Kafka after all retries")

    try:
        async def consume():
            try:
                while True:
                    msg = await consumer.getone()
                    data = json.loads(msg.value.decode("utf-8"))
                    logger.info(f"Received message from Kafka: {data}")
                    body = (
                        f"New post created!\n\n"
                        f"ID: {data['id']}\n"
                        f"Content: {data['content']}\n"
                        f"Author: {data['author']}"
                    )
                    await send_email(body)
            except Exception as e:
                logger.error(f"Error consuming message: {e}")
                raise

        task = asyncio.create_task(consume())
        logger.info("Kafka consumer task started")
        yield
        task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            logger.info("Kafka consumer task cancelled")
    finally:
        if consumer:
            await consumer.stop()
            logger.info("Kafka consumer stopped")


app = FastAPI(lifespan=consume_kafka)

@app.get("/")
async def root():
    return {"message": "Notifications service is running"}