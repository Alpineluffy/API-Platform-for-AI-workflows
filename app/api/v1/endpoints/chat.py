from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse

from app.schemas.chat import ChatRequest, ChatResponse
from app.services.llm_service import LLMService

router = APIRouter(tags=["Chat"])


@router.post("", response_model=ChatResponse)
async def create_chat_completion(request: ChatRequest):
    """
    Generate a chat completion.
    Automatically handles streaming if request.stream == True.
    """
    try:
        if request.stream:
            return StreamingResponse(
                LLMService.stream_chat_completion(request), 
                media_type="text/event-stream"
            )
            
        return await LLMService.generate_chat_completion(request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
