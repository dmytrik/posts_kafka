import json
import asyncio
import logging

from aiokafka import AIOKafkaConsumer

from email_service import send_email


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

consumer = AIOKafkaConsumer(
                    "post_created",
                    bootstrap_servers="kafka:9092",
                    group_id="notification_group",
                    auto_offset_reset="earliest"
                )

async def connect_kafka():
    max_retries = 5
    retry_delay = 5

    for attempt in range(max_retries):
        try:
            logger.info(f"Connecting to Kafka... Attempt {attempt + 1}")
            await consumer.start()
            logger.info("Successfully connected to Kafka")
            break
        except Exception as e:
            logger.error(f"Attempt {attempt + 1} failed: {e}")
            if attempt < max_retries - 1:
                await asyncio.sleep(retry_delay)
            else:
                raise Exception("Failed to connect to Kafka after all retries")


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
