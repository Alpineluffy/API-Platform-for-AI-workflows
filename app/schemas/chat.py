from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum


# ── Enums ────────────────────────────────────────────────
class Role(str, Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"


class ChatModel(str, Enum):
    GPT_4O = "gpt-4o"
    GPT_4O_MINI = "gpt-4o-mini"
    GPT_4_TURBO = "gpt-4-turbo"
    GPT_35_TURBO = "gpt-3.5-turbo"


# ── Request ──────────────────────────────────────────────
class Message(BaseModel):
    role: Role
    content: str


class ChatRequest(BaseModel):
    model: ChatModel = ChatModel.GPT_4O_MINI
    messages: list[Message] = Field(..., min_length=1)
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    max_tokens: Optional[int] = Field(default=None, ge=1, le=128000)
    stream: bool = False
    top_p: float = Field(default=1.0, ge=0.0, le=1.0)


# ── Response ─────────────────────────────────────────────
class Usage(BaseModel):
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int


class Choice(BaseModel):
    index: int
    message: Message
    finish_reason: str


class ChatResponse(BaseModel):
    id: str
    model: str
    choices: list[Choice]
    usage: Usage
    created: int
