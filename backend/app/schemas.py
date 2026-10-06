"""Request/response models shared across the API."""

from enum import Enum

from pydantic import BaseModel, Field, field_validator

from app.core.config import settings


class ScanSource(str, Enum):
    """Where the scanned content came from (the PDF input list)."""

    TEXT = "text"
    WEB = "web"
    EMAIL = "email"
    PDF = "pdf"
    CODE = "code"
    API = "api"
    IMAGE = "image"


class Verdict(str, Enum):
    """Final firewall verdict (matches the frontend VERDICT constant)."""

    SAFE = "safe"
    BLOCKED = "blocked"


class ScanRequest(BaseModel):
    """Content to be scanned by the firewall."""

    content: str = Field(..., description="Text to scan for prompt injection.")
    source: ScanSource = Field(
        ScanSource.TEXT, description="Where the content came from."
    )

    @field_validator("content")
    @classmethod
    def content_must_not_be_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("content must not be empty")
        return v

    @field_validator("content")
    @classmethod
    def content_must_not_be_too_large(cls, v: str) -> str:
        if len(v) > settings.MAX_CONTENT_LENGTH_CHARS:
            raise ValueError(
                f"content must be at most {settings.MAX_CONTENT_LENGTH_CHARS} characters"
            )
        return v


class ScanResponse(BaseModel):
    """Firewall verdict — field names match what the React frontend expects."""

    verdict: Verdict
    attackType: str | None = Field(
        None, description="Attack type, e.g. 'Secret Extraction' (BLOCKED only)."
    )
    reason: str = Field(..., description="Human-readable explanation.")
    confidence: float = Field(
        ...,
        ge=0.0,
        le=100.0,
        description="Confidence as a percentage (0-100).",
    )


# ----------------------------------------------------------------- Way 2 agent
class AgentSource(BaseModel):
    """One source the agent fetches from."""

    type: str = Field(..., description="'url' or 'folder'.")
    value: str = Field(..., description="The URL or the folder path.")
    label: str | None = Field(None, description="Optional display label.")


class AgentRunRequest(BaseModel):
    """Sources for one agent run. Empty -> the sample folder is used."""

    sources: list[AgentSource] = Field(default_factory=list)


class AgentSummary(BaseModel):
    """Dashboard counts for a run."""

    fetched: int = 0
    blocked: int = 0
    passed: int = 0
    flagged: int = 0
    errors: int = 0


class AgentItemResult(BaseModel):
    """Firewall outcome for one fetched item."""

    source: str = ""
    label: str = ""
    verdict: Verdict
    attackType: str | None = None
    reason: str = ""
    confidence: float = 0.0
    action: str = ""
    blocked: bool = False


class AgentRunResponse(BaseModel):
    """Result of one agent pass."""

    summary: AgentSummary
    results: list[AgentItemResult] = Field(default_factory=list)
    errors: list[str] = Field(default_factory=list)