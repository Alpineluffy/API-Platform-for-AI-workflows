from fastapi import APIRouter, HTTPException

from app.schemas.embeddings import EmbeddingRequest, EmbeddingResponse
from app.services.llm_service import LLMService

router = APIRouter(tags=["Embeddings"])


@router.post("", response_model=EmbeddingResponse)
async def create_embeddings(request: EmbeddingRequest):
    """
    Generate vector embeddings for input text.
    """
    try:
        return await LLMService.generate_embeddings(request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
