from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum


# ── Enums ────────────────────────────────────────────────
class EmbeddingModel(str, Enum):
    TEXT_EMBEDDING_3_SMALL = "text-embedding-3-small"
    TEXT_EMBEDDING_3_LARGE = "text-embedding-3-large"
    TEXT_EMBEDDING_ADA_002 = "text-embedding-ada-002"


# ── Request ──────────────────────────────────────────────
class EmbeddingRequest(BaseModel):
    model: EmbeddingModel = EmbeddingModel.TEXT_EMBEDDING_3_SMALL
    input: str | list[str] = Field(..., description="Text or list of texts to embed")
    dimensions: Optional[int] = Field(default=None, ge=1, le=3072)


# ── Response ─────────────────────────────────────────────
class EmbeddingData(BaseModel):
    object: str = "embedding"
    embedding: list[float]
    index: int


class EmbeddingUsage(BaseModel):
    prompt_tokens: int
    total_tokens: int


class EmbeddingResponse(BaseModel):
    object: str = "list"
    data: list[EmbeddingData]
    model: str
    usage: EmbeddingUsage
