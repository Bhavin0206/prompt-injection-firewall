"""FastAPI entry point — the API layer of the Prompt Injection Firewall."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import health
from app.core.config import settings

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    description="An AI firewall that detects and neutralizes prompt injections "
    "before they reach an AI agent.",
)

# Allow the React dev server to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(health.router)
# app.include_router(scan.router, prefix=settings.API_PREFIX)   # added later
# app.include_router(agent.router, prefix=settings.API_PREFIX)  # added later


@app.get("/")
def root() -> dict:
    return {
        "service": settings.APP_NAME,
        "version": settings.VERSION,
        "docs": "/docs",
        "health": "/health",
    }
