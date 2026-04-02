from fastapi import APIRouter

from app.api.v1.endpoints import health, chat, embeddings, ws

api_router = APIRouter()

# ── Health ───────────────────────────────────────────────
api_router.include_router(health.router)

# ── WebSockets ───────────────────────────────────────────
api_router.include_router(ws.router, prefix="/ws")

# ── Core AI ──────────────────────────────────────────────
api_router.include_router(chat.router, prefix="/chat/completions")
api_router.include_router(embeddings.router, prefix="/embeddings")

# ── Async Jobs ───────────────────────────────────────────
from app.api.v1.endpoints import jobs
api_router.include_router(jobs.router, prefix="/jobs")
