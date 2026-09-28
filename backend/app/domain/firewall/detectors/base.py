"""Detector base contract.

Every detector (rule-based, LLM, embeddings, …) implements the Detector ABC
and returns the SAME DetectorResult shape. The decision engine only speaks
this contract, so adding a new detector never changes the engine.

Confidence scale: detectors report 0..1 (the engine compares against
settings.DETECTOR_CONFIDENCE_THRESHOLD). The API layer converts to the
0-100 percentage the frontend expects.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field


@dataclass
class DetectorResult:
    """The single output shape every detector returns."""

    # Which detector produced this result (e.g. "rule", "llm", "embedding").
    detector_name: str

    # True when this detector thinks the content is malicious.
    is_attack: bool = False

    # Attack type (one of the 9) — set when is_attack is True.
    attack_type: str | None = None

    # Detector's confidence that the content is malicious (0..1).
    confidence: float = 0.0

    # Which specific patterns/signals matched (feeds the reason text).
    matched_patterns: list[str] = field(default_factory=list)

    # Free-form detail the detector wants to surface.
    details: str = ""

    @property
    def name(self) -> str:
        return self.detector_name

    @classmethod
    def no_hit(cls, detector_name: str, details: str = "") -> "DetectorResult":
        """A clean result (SAFE side)."""
        return cls(detector_name=detector_name, details=details)

    @classmethod
    def hit(
        cls,
        detector_name: str,
        attack_type: str,
        confidence: float,
        matched_patterns: list[str] | None = None,
        details: str = "",
    ) -> "DetectorResult":
        """A malicious result (BLOCKED side)."""
        return cls(
            detector_name=detector_name,
            is_attack=True,
            attack_type=attack_type,
            confidence=confidence,
            matched_patterns=matched_patterns or [],
            details=details,
        )


class Detector(ABC):
    """Base contract: implement `detect` and the detector is pluggable."""

    # Human-readable detector id, e.g. "rule", "llm", "embedding".
    name: str = "base"

    @abstractmethod
    async def detect(self, content: str) -> DetectorResult:
        """Analyze content and return a DetectorResult.

        Implementations should prefer returning a result over raising —
        the engine must be able to keep scanning on partial failures.
        """