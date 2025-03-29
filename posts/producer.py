from aiokafka import AIOKafkaProducer


async def get_kafka_producer():
    producer = AIOKafkaProducer(bootstrap_servers="kafka-server:9092")
    await producer.start()
    try:
        yield producer
    finally:
        await producer.stop()
