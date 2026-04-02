from openai import AsyncOpenAI

from app.core.config import get_settings
from app.schemas.chat import ChatRequest, ChatResponse
from app.schemas.embeddings import EmbeddingRequest, EmbeddingResponse

settings = get_settings()

client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)


class LLMService:
    """Service wrapper for interacting with the OpenAI API."""

    @staticmethod
    async def generate_chat_completion(request: ChatRequest) -> ChatResponse:
        """Generate a chat completion using the OpenAI API."""
        # Convert Pydantic models to dicts for the OpenAI client
        messages = [{"role": msg.role.value, "content": msg.content} for msg in request.messages]
        
        response = await client.chat.completions.create(
            model=request.model.value,
            messages=messages,
            temperature=request.temperature,
            max_tokens=request.max_tokens,
            top_p=request.top_p,
            stream=request.stream,
        )
        
        # We can just return the pydantic model parsed from the raw dict
        # AsyncOpenAI v1+ returns Pydantic-like objects, we need to convert them to our internal schemas
        # or we could've just returned their schema directly, but keeping our own contract is safer for decoupling.
        return ChatResponse.model_validate(response.model_dump())

    @staticmethod
    async def generate_embeddings(request: EmbeddingRequest) -> EmbeddingResponse:
        """Generate embeddings using the OpenAI API."""
        response = await client.embeddings.create(
            model=request.model.value,
            input=request.input,
            dimensions=request.dimensions,
        )
        
        return EmbeddingResponse.model_validate(response.model_dump())
