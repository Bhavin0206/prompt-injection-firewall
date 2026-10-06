"""Agent state — the shared data passed between graph nodes (Way 2).

The graph nodes read from and write to this state:
    fetch  -> fills `items`
    scan   -> fills `results`
    decide -> sets each result's action
    summarize -> fills `summary`

Fields:
    sources  : what to fetch (urls / folders)
    items    : content the agent fetched (not yet scanned)
    results  : firewall verdict per item
    summary  : counts for the dashboard
    errors   : non-fatal problems (a bad source must not kill the run)
"""

from __future__ import annotations

import operator
from typing import Annotated, TypedDict


class SourceSpec(TypedDict, total=False):
    """One configured source ("doorway") the agent fetches from."""

    type: str  # "url" | "folder"
    value: str  # the URL or the folder path
    label: str  # optional display label


class FetchedItem(TypedDict):
    """Content the agent fetched, ready to be scanned."""

    source: str  # source type, e.g. "url" / "folder"
    label: str  # e.g. the URL or "email-01.eml"
    content: str  # the text to scan


class ItemResult(TypedDict, total=False):
    """Firewall outcome for one fetched item."""

    source: str
    label: str
    verdict: str  # "blocked" | "safe"
    attack_type: str | None
    reason: str
    confidence: float  # 0-100
    action: str  # "block" | "flag" | "pass"
    blocked: bool  # True only for a hard block


class Summary(TypedDict, total=False):
    """Counts shown on the dashboard."""

    fetched: int
    blocked: int
    passed: int
    flagged: int
    errors: int


class AgentState(TypedDict, total=False):
    """The graph state. `errors` accumulates across nodes; others replace."""

    sources: list[SourceSpec]
    items: list[FetchedItem]
    results: list[ItemResult]
    summary: Summary
    errors: Annotated[list[str], operator.add]


def initial_state(sources: list[SourceSpec] | None = None) -> AgentState:
    """A fresh state for one agent run."""
    return {
        "sources": list(sources or []),
        "items": [],
        "results": [],
        "summary": {"fetched": 0, "blocked": 0, "passed": 0, "flagged": 0, "errors": 0},
        "errors": [],
    }
