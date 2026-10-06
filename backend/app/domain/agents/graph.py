"""Agent graph (Way 2) — fetch -> scan -> decide -> summarize.

Built with LangGraph's StateGraph (1.x API) and compiled once.

Node progress:
    fetch     -> DONE (Task 7)
    scan      -> stub (Task 8)
    decide    -> stub (Task 9)
    summarize -> stub (Task 10)
"""

from __future__ import annotations

from langgraph.graph import END, START, StateGraph

from app.domain.agents.state import AgentState, FetchedItem, ItemResult
from app.domain.agents.tools.fetch_web import fetch_web
from app.domain.agents.tools.read_files import read_folder
from app.domain.firewall.engine import Verdict, get_engine
from app.domain.firewall.neutralizer import get_neutralizer


# ---------------------------------------------------------------- fetch
def fetch_node(state: AgentState) -> dict:
    """Fetch content from every configured source.

    Each source is {type: "url"|"folder", value: ...}. A source that fails is
    recorded in `errors` and skipped — one bad source must not stop the run.
    """
    items: list[FetchedItem] = []
    errors: list[str] = []

    for source in state.get("sources", []):
        source_type = str(source.get("type", "")).lower()
        value = str(source.get("value", ""))

        try:
            if source_type == "url":
                items.append(fetch_web(value))
            elif source_type == "folder":
                items.extend(read_folder(value))
            else:
                errors.append(f"Unknown source type: {source_type!r}")
        except Exception as exc:  # noqa: BLE001 - keep going on a bad source
            errors.append(f"{source_type} '{value}': {exc}")

    return {"items": items, "errors": errors}


# ---------------------------------------------------------------- stubs
async def scan_node(state: AgentState) -> dict:
    """Run every fetched item through the firewall core (same code as Way 1).

    Reuses the shared DecisionEngine — no detection logic is duplicated.
    A single item that fails is recorded in `errors` and skipped.
    """
    engine = get_engine()
    results: list[ItemResult] = []
    errors: list[str] = []

    for item in state.get("items", []):
        label = item.get("label", "?")
        try:
            verdict = await engine.scan(item.get("content", ""))
            results.append(
                {
                    "source": item.get("source", ""),
                    "label": label,
                    "verdict": "blocked" if verdict.is_attack else "safe",
                    "attack_type": verdict.attack_type,
                    "reason": verdict.reason,
                    "confidence": round(verdict.confidence * 100, 1),
                }
            )
        except Exception as exc:  # noqa: BLE001 - keep scanning the rest
            errors.append(f"scan failed for '{label}': {exc}")

    return {"results": results, "errors": errors}


def decide_node(state: AgentState) -> dict:
    """Apply the neutralizer to each scan result: action + human message.

    Marks every item as blocked / passed (flag = passed with a warning) and
    keeps the readable reason for blocked items.
    """
    neutralizer = get_neutralizer()
    updated: list[ItemResult] = []

    for result in state.get("results", []):
        verdict = Verdict(
            is_attack=result.get("verdict") == "blocked",
            attack_type=result.get("attack_type"),
            confidence=(result.get("confidence") or 0.0) / 100.0,
            reason=result.get("reason", ""),
        )
        outcome = neutralizer.neutralize(verdict)
        updated.append(
            {
                **result,
                "action": outcome.action.value,
                "blocked": outcome.blocked,
                "reason": outcome.message,
            }
        )

    return {"results": updated}


def summarize_node(state: AgentState) -> dict:
    """Build the dashboard counts for the run.

    The per-item results are already in `state["results"]` (each with verdict,
    action, reason and confidence) — the dashboard reads them directly.
    """
    items = state.get("items", [])
    results = state.get("results", [])
    errors = state.get("errors", [])

    blocked = sum(1 for r in results if r.get("action") == "block")
    flagged = sum(1 for r in results if r.get("action") == "flag")
    passed = sum(1 for r in results if r.get("action") == "pass")

    return {
        "summary": {
            "fetched": len(items),
            "blocked": blocked,
            "passed": passed,
            "flagged": flagged,
            "errors": len(errors),
        }
    }


# ---------------------------------------------------------------- graph
def build_graph():
    """Create and compile the agent graph."""
    graph = StateGraph(AgentState)

    graph.add_node("fetch", fetch_node)
    graph.add_node("scan", scan_node)
    graph.add_node("decide", decide_node)
    graph.add_node("summarize", summarize_node)

    graph.add_edge(START, "fetch")
    graph.add_edge("fetch", "scan")
    graph.add_edge("scan", "decide")
    graph.add_edge("decide", "summarize")
    graph.add_edge("summarize", END)

    return graph.compile()


# Compiled once and reused across runs.
agent_graph = build_graph()
