import json
import logging
import asyncio
from aiokafka import AIOKafkaConsumer

from app.core.config import get_settings
from app.db.session import async_session
from app.jobs.models import Job, JobStatus

settings = get_settings()
logger = logging.getLogger(__name__)

async def process_job(message: dict):
    """Simulates a long-running agent or AI task."""
    job_id = message.get("job_id")
    task_name = message.get("task_name")
    
    async with async_session() as db:
        # Fetch the job
        job = await db.get(Job, job_id)
        if not job:
            logger.error(f"Job {job_id} not found in DB.")
            return

        # Update status to RUNNING
        job.status = JobStatus.RUNNING
        await db.commit()

        try:
            # --- Simulating backend AI Task Work ---
            logger.info(f"Worker starting task: {task_name} (ID: {job_id})")
            await asyncio.sleep(5)  # Simulated delay representing long-running LLM/agent call
            
            # Save the result
            job.result = {
                "success": True, 
                "output": f"Simulated result for {task_name}",
                "simulated_metrics": {"steps": 5}
            }
            job.status = JobStatus.COMPLETED
            logger.info(f"Worker completed task: {task_name}")

        except Exception as e:
            job.status = JobStatus.FAILED
            job.result = {"error": str(e)}
            logger.error(f"Worker failed task: {task_name} - {e}")
            
        finally:
            await db.commit()


async def start_kafka_worker():
    """Background loop that polls Kafka and processes jobs."""
    consumer = AIOKafkaConsumer(
        "ai_platform_jobs",
        bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
        group_id="async_agent_workers",
        value_deserializer=lambda m: json.loads(m.decode("utf-8")),
        auto_offset_reset="earliest"
    )
    
    try:
        await consumer.start()
        logger.info("Kafka async worker started listening to 'ai_platform_jobs'")
        
        async for msg in consumer:
            message = msg.value
            logger.info(f"Kafka worker received message: {message}")
            
            # Fire and forget the processor so it doesn't block polling, 
            # or await it for strict sequential processing per partition
            # We'll use asyncio.create_task for concurrent async workers
            asyncio.create_task(process_job(message))
            
    except asyncio.CancelledError:
        logger.info("Kafka worker loop cancelled.")
    except Exception as e:
        logger.error(f"Kafka worker died: {e}")
    finally:
        await consumer.stop()
