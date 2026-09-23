"""Request/response models shared across the API."""

from pydantic import BaseModel


class ScanRequest(BaseModel):
    """Content to be scanned by the firewall."""

    content: str
    source: str = "text"  # text | web | email | pdf | image | api | code


class ScanResponse(BaseModel):
    """Firewall verdict."""

    verdict: str  # "safe" | "blocked"
    reason: str
    attack_type: str | None = None
    confidence: float = 0.0
