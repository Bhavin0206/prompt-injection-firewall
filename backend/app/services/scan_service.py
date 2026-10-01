"""Scan service — orchestrates one scan. No AI logic here (thin layer).

Flow: validate -> engine (detect) -> neutralizer (action + message) -> response.

The API route only needs this service; all detection lives in the domain layer.
"""

from __future__ import annotations

from app.domain.firewall.engine import DecisionEngine
from app.domain.firewall.neutralizer import Neutralizer
from app.schemas import ScanRequest, ScanResponse
from app.schemas import Verdict as VerdictEnum


class ScanService:
    """Coordinates the firewall pieces for a single scan request."""

    def __init__(
        self,
        engine: DecisionEngine | None = None,
        neutralizer: Neutralizer | None = None,
    ) -> None:
        # Created once and reused (the LLM client should not be rebuilt per call).
        self._engine = engine or DecisionEngine()
        self._neutralizer = neutralizer or Neutralizer()

    async def scan(self, request: ScanRequest) -> ScanResponse:
        # 1. validate: done by ScanRequest (pydantic) before we get here.
        # 2. detect: run the detectors and combine into one verdict.
        verdict = await self._engine.scan(request.content)

        # 3. neutralize: decide the action + build the human message.
        outcome = self._neutralizer.neutralize(verdict)

        # 4. shape the API response.
        return ScanResponse(
            verdict=VerdictEnum.BLOCKED if verdict.is_attack else VerdictEnum.SAFE,
            attackType=verdict.attack_type,
            reason=outcome.message,
            confidence=round(verdict.confidence * 100, 1),
        )


# ---- shared instance (built once, reused by every request) ----
_service: ScanService | None = None


def get_scan_service() -> ScanService:
    """FastAPI dependency: returns the shared ScanService instance."""
    global _service
    if _service is None:
        _service = ScanService()
    return _service
