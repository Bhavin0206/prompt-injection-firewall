"""Application configuration (env vars, constants)."""

import os

from dotenv import load_dotenv

load_dotenv()


def _env_int(name: str, default: int) -> int:
    try:
        return int(os.getenv(name, str(default)))
    except ValueError:
        return default


def _env_float(name: str, default: float) -> float:
    try:
        return float(os.getenv(name, str(default)))
    except ValueError:
        return default


# Supported LLM providers.
LLM_PROVIDER_GEMINI = "gemini"
LLM_PROVIDER_OPENAI = "openai"


class Settings:
    # ---- App ----
    APP_NAME: str = "Prompt Injection Firewall API"
    VERSION: str = "0.1.0"
    API_PREFIX: str = "/api"
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

    # Frontend dev servers (Vite) — allowed by CORS
    CORS_ORIGINS: list[str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5174",
    ]

    # ---- LLM ----
    LLM_PROVIDER: str = os.getenv("LLM_PROVIDER", LLM_PROVIDER_GEMINI)
    LLM_API_KEY: str = os.getenv("LLM_API_KEY", "")

    # Model names, per provider. LLM_MODEL explicitly overrides both.
    LLM_MODEL: str = os.getenv("LLM_MODEL", "")
    GEMINI_MODEL: str = os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    # LLM call behavior
    LLM_TIMEOUT_SECONDS: int = _env_int("LLM_TIMEOUT_SECONDS", 60)
    LLM_MAX_TOKENS: int = _env_int("LLM_MAX_TOKENS", 512)
    LLM_TEMPERATURE: float = _env_float("LLM_TEMPERATURE", 0.0)  # deterministic

    # ---- Firewall thresholds ----
    # Detector hits below this confidence (0..1) are ignored — lowers false positives.
    DETECTOR_CONFIDENCE_THRESHOLD: float = _env_float(
        "DETECTOR_CONFIDENCE_THRESHOLD", 0.60
    )
    # Refuse content larger than this (characters) with a 400.
    MAX_CONTENT_LENGTH_CHARS: int = _env_int("MAX_CONTENT_LENGTH_CHARS", 20000)

    # ---- Local vector DB ----
    CHROMA_DIR: str = os.getenv("CHROMA_DIR", "data/chroma")

    # ---- Derived helpers ----
    @property
    def llm_provider(self) -> str:
        """Normalized provider name (e.g. 'GEMINI' -> 'gemini')."""
        return self.LLM_PROVIDER.strip().lower()

    @property
    def llm_model(self) -> str:
        """The model name for the configured provider."""
        if self.LLM_MODEL:
            return self.LLM_MODEL
        if self.llm_provider == LLM_PROVIDER_OPENAI:
            return self.OPENAI_MODEL
        return self.GEMINI_MODEL

    @property
    def has_llm_key(self) -> bool:
        """True when a real API key is configured (placeholder doesn't count)."""
        return bool(self.LLM_API_KEY) and self.LLM_API_KEY != "your_api_key_here"


settings = Settings()