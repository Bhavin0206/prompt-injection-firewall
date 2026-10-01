"""Decision engine — combines detector results into ONE verdict.

Rule (from the plan): any STRONG hit -> BLOCKED, else SAFE.
A "strong hit" = a detector reported is_attack with confidence >= threshold.

Defence in depth: detectors fail soft (they return no_hit instead of raising),
so if the LLM detector is unavailable or errors, the rule detector still decides.
"""

from __future__ import annotations

import asyncio
from dataclasses import dataclass, field

from app.core.config import settings
from app.domain.firewall.detectors.base import Detector, DetectorResult
from app.domain.firewall.detectors.llm_detector import LLMDetector
from app.domain.firewall.detectors.rule_detector import RuleDetector


@dataclass
class Verdict:
    """The engine's final decision."""

    is_attack: bool  # True = BLOCKED, False = SAFE
    attack_type: str | None
    confidence: float  # 0..1 (attack confidence, or safe confidence when clean)
    reason: str
    detector: str | None = None  # which detector decided (None when SAFE)
    results: list[DetectorResult] = field(default_factory=list)  # raw results


def default_detectors() -> list[Detector]:
    """The detectors the engine runs by default (order doesn't matter)."""
    return [RuleDetector(), LLMDetector()]


class DecisionEngine:
    """Runs every detector and folds their results into one Verdict."""

    def __init__(
        self,
        detectors: list[Detector] | None = None,
        threshold: float | None = None,
    ) -> None:
        self._detectors = detectors if detectors is not None else default_detectors()
        self._threshold = (
            threshold if threshold is not None else settings.DETECTOR_CONFIDENCE_THRESHOLD
        )

    async def scan(self, content: str) -> Verdict:
        """Run all detectors (in parallel) and decide."""
        results = await asyncio.gather(
            *(self._safe_detect(d, content) for d in self._detectors)
        )
        return self._decide(list(results))

    async def _safe_detect(self, detector: Detector, content: str) -> DetectorResult:
        """Run one detector; a failure becomes a no-hit so others still decide."""
        try:
            return await detector.detect(content)
        except Exception as exc:  # noqa: BLE001 - never let one detector crash the scan
            return DetectorResult.no_hit(
                detector.name, details=f"{detector.name} detector failed: {exc}"
            )

    # ---- decision ----
    def _decide(self, results: list[DetectorResult]) -> Verdict:
        # Any hit at/above the threshold blocks.
        strong = [r for r in results if r.is_attack and r.confidence >= self._threshold]
        if strong:
            best = max(strong, key=lambda r: r.confidence)
            return Verdict(
                is_attack=True,
                attack_type=best.attack_type,
                confidence=round(best.confidence, 2),
                reason=self._attack_reason(best),
                detector=best.detector_name,
                results=results,
            )

        # No strong hit -> SAFE. Safe-confidence = 1 - strongest weak signal.
        strongest_signal = max(
            (r.confidence for r in results if r.is_attack), default=0.0
        )
        safe_confidence = round(max(0.0, 1.0 - strongest_signal), 2)
        # Prefer the most descriptive reason (LLM runs last, so check reversed).
        reason = next((r.details for r in reversed(results) if r.details), "") or (
            "No prompt-injection detected."
        )
        return Verdict(
            is_attack=False,
            attack_type=None,
            confidence=safe_confidence,
            reason=reason,
            detector=None,
            results=results,
        )

    @staticmethod
    def _attack_reason(result: DetectorResult) -> str:
        if result.details:
            return result.details
        if result.matched_patterns:
            return f"Matched suspicious pattern(s): {', '.join(result.matched_patterns)}"
        return f"Detected {result.attack_type}."
