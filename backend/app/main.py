"""FastAPI entry point — the API layer of the Prompt Injection Firewall."""

import logging

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.routes import health, scan
from app.core.config import settings

logger = logging.getLogger("firewall")

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
app.include_router(scan.router, prefix=settings.API_PREFIX)
# app.include_router(agent.router, prefix=settings.API_PREFIX)  # added later (Way 2)


# ---- Clean error responses (no internals leaked) ----
@app.exception_handler(RequestValidationError)
async def validation_error_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    """Bad input -> 422 with a tidy body."""
    return JSONResponse(
        status_code=422,
        content={
            "error": "invalid_request",
            "detail": [
                {"field": ".".join(str(p) for p in err["loc"][1:]), "message": err["msg"]}
                for err in exc.errors()
            ],
        },
    )


@app.exception_handler(Exception)
async def unhandled_error_handler(request: Request, exc: Exception) -> JSONResponse:
    """Unexpected error -> 500 with a safe message (details stay in the logs)."""
    logger.exception("Unhandled error on %s", request.url.path)
    return JSONResponse(
        status_code=500,
        content={
            "error": "internal_error",
            "detail": "Something went wrong while scanning. Please try again.",
        },
    )


@app.get("/")
def root() -> dict:
    return {
        "service": settings.APP_NAME,
        "version": settings.VERSION,
        "docs": "/docs",
        "health": "/health",
    }
