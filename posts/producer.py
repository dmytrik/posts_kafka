import logging

from aiokafka import AIOKafkaProducer


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

producer = None

async def init_kafka_producer():

    global producer
    producer = AIOKafkaProducer(bootstrap_servers="kafka:9092")
    try:
        await producer.start()
        logger.info("Kafka producer started successfully")
    except Exception as e:
        logger.error(f"Failed to start Kafka producer: {e}")
        raise

async def shutdown_kafka_producer():
    global producer
    if producer:
        await producer.stop()
        logger.info("Kafka producer stopped")
        producer = None

def get_kafka_producer() -> AIOKafkaProducer:
    if not producer:
        raise RuntimeError("Kafka producer is not initialized")
    return producer
