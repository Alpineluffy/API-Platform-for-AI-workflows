from fastapi import APIRouter, HTTPException

from app.schemas.chat import ChatRequest, ChatResponse
from app.services.llm_service import LLMService

router = APIRouter(tags=["Chat"])


@router.post("", response_model=ChatResponse)
async def create_chat_completion(request: ChatRequest):
    """
    Generate a chat completion.
    Streaming is currently disabled (handled via Phase 3 streaming endpoints).
    """
    try:
        if request.stream:
            raise HTTPException(
                status_code=400, 
                detail="Streaming requests must use the streaming endpoint (coming soon)."
            )
            
        return await LLMService.generate_chat_completion(request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
