"""Neutralizer — turns a Verdict into an ACTION + a human-readable message.

Implements the PDF's "neutralize" step. Actions:
    pass  - clean content, let it through to the AI
    flag  - suspicious (below the hard-block bar): pass with a warning
    strip - remove the malicious part, pass the rest (reserved / future)
    block - reject; the AI never sees it

The engine decides *if* it is an attack; the neutralizer decides *what to do*
and writes the message the user sees.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from app.core.config import settings
from app.domain.firewall.engine import Verdict


class Action(str, Enum):
    PASS = "pass"
    FLAG = "flag"
    STRIP = "strip"
    BLOCK = "block"


@dataclass
class Neutralization:
    """What the firewall decided to DO, plus the message for the user."""

    action: Action
    blocked: bool  # True only for a hard block
    message: str


class Neutralizer:
    """Decides the action + writes the human-readable reason."""

    def __init__(self, block_threshold: float | None = None) -> None:
        self._block_threshold = (
            block_threshold
            if block_threshold is not None
            else settings.NEUTRALIZER_BLOCK_THRESHOLD
        )

    def neutralize(self, verdict: Verdict) -> Neutralization:
        # Clean -> pass through.
        if not verdict.is_attack:
            return Neutralization(
                action=Action.PASS,
                blocked=False,
                message=(
                    "No prompt injection detected. "
                    "Content is safe to pass to the AI."
                ),
            )

        attack = verdict.attack_type or "suspicious content"
        confidence = round(verdict.confidence * 100)

        # High confidence -> hard block.
        if verdict.confidence >= self._block_threshold:
            return Neutralization(
                action=Action.BLOCK,
                blocked=True,
                message=(
                    f"Blocked: {attack} detected ({confidence}% confidence). "
                    f"{verdict.reason} Content was not passed to the AI."
                ),
            )

        # Suspicious but not confident enough to hard-block -> flag and pass.
        return Neutralization(
            action=Action.FLAG,
            blocked=False,
            message=(
                f"Flagged as suspicious: possible {attack} "
                f"({confidence}% confidence). {verdict.reason} "
                "Passed with a warning."
            ),
        )
