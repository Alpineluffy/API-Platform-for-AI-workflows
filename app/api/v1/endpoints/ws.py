from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from pydantic import ValidationError
import json

from app.schemas.chat import ChatRequest
from app.services.llm_service import LLMService

router = APIRouter(tags=["WebSockets"])

@router.websocket("/chat")
async def websocket_chat_endpoint(websocket: WebSocket):
    """
    WebSocket endpoint for real-time streaming chat.
    Accepts JSON messages shaped like `ChatRequest`, ignoring the stream flag.
    Returns token chunks directly.
    """
    await websocket.accept()
    try:
        while True:
            # Receive message from user
            data = await websocket.receive_text()
            
            try:
                # Parse and validate the incoming JSON using Pydantic
                request_data = json.loads(data)
                # Force stream to true to ensure we use the backend generator logic effectively
                request_data["stream"] = True 
                chat_request = ChatRequest(**request_data)
                
                # Stream responses back chunks via websocket
                async for chunk in LLMService.stream_chat_completion(chat_request):
                    # We strip the "data: " and "\n\n" since WebSockets don't need SSE wrapping
                    clean_chunk = chunk.removeprefix("data: ").removesuffix("\n\n")
                    await websocket.send_text(clean_chunk)
                    
            except ValidationError as e:
                await websocket.send_json({"error": "Validation Error", "details": e.errors()})
            except Exception as e:
                await websocket.send_json({"error": "Internal Error", "details": str(e)})

    except WebSocketDisconnect:
        # Client gracefully closed the connection
        pass
