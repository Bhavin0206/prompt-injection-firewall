"""Application configuration (env vars, constants)."""

import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    APP_NAME: str = "Prompt Injection Firewall API"
    VERSION: str = "0.1.0"
    API_PREFIX: str = "/api"

    # Frontend dev server (Vite) — allowed by CORS
    CORS_ORIGINS: list[str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ]

    # LLM (set in .env later)
    LLM_PROVIDER: str = os.getenv("LLM_PROVIDER", "gemini")
    LLM_API_KEY: str = os.getenv("LLM_API_KEY", "")

    # Local vector DB
    CHROMA_DIR: str = os.getenv("CHROMA_DIR", "data/chroma")


settings = Settings()
