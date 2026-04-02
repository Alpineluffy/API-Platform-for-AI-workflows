from fastapi import APIRouter

from app.api.v1.endpoints import health, chat, embeddings

api_router = APIRouter()

# ── Health ───────────────────────────────────────────────
api_router.include_router(health.router)

# ── Core AI ──────────────────────────────────────────────
api_router.include_router(chat.router, prefix="/chat/completions")
api_router.include_router(embeddings.router, prefix="/embeddings")
