import json
import logging
from aiokafka import AIOKafkaProducer
from app.core.config import get_settings

settings = get_settings()
logger = logging.getLogger(__name__)

# Global producer instance
producer = None


async def get_producer() -> AIOKafkaProducer:
    """Get or initialize the global Kafka producer."""
    global producer
    if producer is None:
        producer = AIOKafkaProducer(
            bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
            value_serializer=lambda v: json.dumps(v).encode("utf-8"),
        )
        await producer.start()
    return producer


async def stop_producer():
    """Stop the global Kafka producer gracefully."""
    global producer
    if producer is not None:
        await producer.stop()


async def enqueue_job(job_id: str, task_name: str, payload: dict):
    """Enqueue a background job onto the Kafka topic."""
    p = await get_producer()
    message = {
        "job_id": job_id,
        "task_name": task_name,
        "payload": payload,
    }
    await p.send_and_wait("ai_platform_jobs", message)
