"""Rule-based detector — the "quick look" guard.

Fast, free, offline: scans the content for KNOWN bad regex patterns and
reports which attack type each hit belongs to.

Flow (per the Task 4 plan):
    content -> lowercase + collapse spacing -> loop every attack type
    -> collect matches -> score = weight x matches -> sort (highest first)
    -> return the list of hits  ([] = clean by rules)

It also implements the Task 3 Detector contract, so `detect()` returns a
DetectorResult for the decision engine while `scan()` exposes the full hit
list for reason-building.

No API key needed.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

from app.domain.firewall.attack_types import ATTACK_TYPES, compiled_rules
from app.domain.firewall.detectors.base import Detector, DetectorResult


# One attack type that matched.  (The plan's output unit.)
@dataclass
class RuleHit:
    attack_type: str
    matched: list[str] = field(default_factory=list)  # the actual text that matched
    weight: int = 0
    score: int = 0  # weight x number_of_matches

    @property
    def confidence(self) -> float:
        """Map the integer score onto the 0..1 scale the engine threshold uses.

        score 1 (one weak hit) -> 0.57, deliberately just BELOW the 0.60
        threshold so a single weak signal never blocks on its own; stronger
        or repeated signals (score >= 2) cross the threshold.
        """
        return round(min(0.99, 0.45 + 0.12 * self.score), 2)


# Phrases showing the content DISCUSSES an attack (training, docs, examples)
# rather than performing one. Combined with quotes, this avoids flagging
# benign content that merely MENTIONS an attack phrase.
_BENIGN_MENTION_RE = re.compile(
    r"\b(training|learned|learning|teaches|teaching|documentation|docs?|"
    r"example|examples|explain|explains|explaining|article|blog|research|"
    r"tutorial|guide|awareness|write[\s-]?up|report)\b"
    r"[^\u2018\u2019\u201c\u201d'\"]{0,100}?"
    r"[\u2018\u2019\u201c\u201d'\"]"
    r"[^\u2018\u2019\u201c\u201d'\"]{0,80}?"
    r"[\u2018\u2019\u201c\u201d'\"]",
    re.IGNORECASE,
)

# Anything inside single / double / curly quotes.
_QUOTED_RE = re.compile(
    r"[\u2018\u2019\u201c\u201d'\"]([^\u2018\u2019\u201c\u201d'\"]{1,120})"
    r"[\u2018\u2019\u201c\u201d'\"]"
)


class RuleDetector(Detector):
    """Regex/keyword detector implementing the common Detector contract."""

    name = "rule"

    def __init__(self) -> None:
        # Compile every pattern once and GROUP it by attack type, so scanning
        # runs each regex exactly once (not once per attack type).
        self._rules: dict[str, list[tuple[str, re.Pattern[str]]]] = {
            attack.name: [] for attack in ATTACK_TYPES
        }
        for attack, pattern in compiled_rules():
            self._rules[attack.name].append((attack.name, pattern))

    @staticmethod
    def _normalize(content: str) -> str:
        """Lower-case + collapse whitespace runs (handles CASE + SPACING)."""
        return re.sub(r"\s+", " ", content.lower()).strip()

    def scan(self, content: str) -> list[RuleHit]:
        """Return every attack type that matched, strongest first (plan output)."""
        text = self._normalize(content)

        # Benign-mention guard: when the content is clearly DISCUSSING an
        # attack (training/docs/example) AND the phrase sits inside quotes,
        # treat it as a mention, not an attack (reduces false positives).
        benign_mention = bool(_BENIGN_MENTION_RE.search(text))
        quoted_spans = [
            (m.start(1), m.end(1)) for m in _QUOTED_RE.finditer(text)
        ]

        hits: list[RuleHit] = []

        for attack in ATTACK_TYPES:
            matched: list[str] = []
            seen: set[str] = set()

            for _, pattern in self._rules[attack.name]:
                for found in pattern.finditer(text):
                    frag = found.group(0)
                    if frag in seen:
                        continue
                    if benign_mention and any(
                        start <= found.start() < end for start, end in quoted_spans
                    ):
                        continue  # quoted/reported mention, not an attack
                    seen.add(frag)
                    matched.append(frag)

            if matched:
                hits.append(
                    RuleHit(
                        attack_type=attack.name,
                        matched=matched,
                        weight=attack.weight,
                        score=attack.weight * len(matched),
                    )
                )

        # Step 5: sort by score, highest first.
        hits.sort(key=lambda h: h.score, reverse=True)
        return hits

    async def detect(self, content: str) -> DetectorResult:
        """Detector contract: fold the hit list into ONE DetectorResult."""
        hits = self.scan(content)
        if not hits:
            return DetectorResult.no_hit(self.name, details="No rule patterns matched.")

        top = hits[0]
        return DetectorResult.hit(
            detector_name=self.name,
            attack_type=top.attack_type,
            confidence=top.confidence,
            matched_patterns=top.matched,
            details=f"{len(hits)} rule type(s) matched: "
            + ", ".join(f"{h.attack_type}({h.score})" for h in hits),
        )
