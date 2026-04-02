from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Any

from app.schemas.jobs import JobCreateRequest, JobStatusResponse
from app.jobs.models import Job, JobStatus
from app.jobs.producer import enqueue_job
from app.db.session import get_db

router = APIRouter(tags=["Async Jobs"])


@router.post("/", response_model=JobStatusResponse)
async def create_job(request: JobCreateRequest, db: AsyncSession = Depends(get_db)):
    """
    Submit a long-running task to the background queue.
    Returns immediately with a Tracking status.
    """
    job = Job(
        task_name=request.task_name,
        payload=request.payload,
        status=JobStatus.PENDING,
    )
    db.add(job)
    await db.commit()
    await db.refresh(job)

    # Dispatch to Kafka
    await enqueue_job(str(job.id), job.task_name, job.payload or {})

    return job


@router.get("/{job_id}", response_model=JobStatusResponse)
async def get_job_status(job_id: str, db: AsyncSession = Depends(get_db)):
    """
    Poll the status of an async job.
    """
    job = await db.get(Job, job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
        
    return job
