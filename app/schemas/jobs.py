from pydantic import BaseModel
from typing import Optional, Any
from uuid import UUID
from datetime import datetime
from app.jobs.models import JobStatus

class JobCreateRequest(BaseModel):
    task_name: str
    payload: Optional[dict[str, Any]] = None

class JobStatusResponse(BaseModel):
    id: UUID
    task_name: str
    status: JobStatus
    result: Optional[dict[str, Any]] = None
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }
