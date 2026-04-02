from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import get_settings
from app.api.v1.router import api_router
from app.db.session import engine

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup / shutdown lifecycle hook."""
    # ── Startup ──────────────────────────────────────────
    # Engine is already created; nothing extra needed for now.
    yield
    # ── Shutdown ─────────────────────────────────────────
    await engine.dispose()


app = FastAPI(
    title=settings.APP_NAME,
    description="A scalable API platform for AI workflows — chat, embeddings, and agents.",
    version=settings.APP_VERSION,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

# ── CORS ─────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Routers ──────────────────────────────────────────────
app.include_router(api_router, prefix=settings.API_V1_PREFIX)

# Mount health at root level too for k8s / ECS probes
from app.api.v1.endpoints.health import router as health_router  # noqa: E402

app.include_router(health_router)
