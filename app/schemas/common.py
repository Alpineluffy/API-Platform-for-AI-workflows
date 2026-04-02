from pydantic import BaseModel, Field
from datetime import datetime


class ErrorResponse(BaseModel):
    """Standard error response format."""

    error: str
    message: str
    status_code: int
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class PaginatedResponse(BaseModel):
    """Wrapper for paginated list responses."""

    data: list
    total: int
    page: int = 1
    per_page: int = 20
    has_more: bool = False
