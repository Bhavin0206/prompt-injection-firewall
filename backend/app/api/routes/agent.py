"""POST /agent/run — run the Way 2 agent over some sources.

The agent fetches content from the sources, scans every item with the SAME
firewall core, and returns a dashboard-ready summary.
"""

from fastapi import APIRouter

from app.core.config import settings
from app.domain.agents.runner import run_agent
from app.schemas import (
    AgentItemResult,
    AgentRunRequest,
    AgentRunResponse,
    AgentSummary,
    Verdict,
)

router = APIRouter(tags=["agent"])


@router.post(
    "/agent/run",
    response_model=AgentRunResponse,
    summary="Run the agent over sources",
    response_description="Dashboard counts + per-item firewall results.",
)
async def run_agent_endpoint(request: AgentRunRequest) -> AgentRunResponse:
    """Fetch from the sources and scan everything automatically."""
    # No sources given -> fall back to the bundled sample folder (demo friendly).
    sources = [source.model_dump() for source in request.sources]
    if not sources:
        sources = [{"type": "folder", "value": settings.SAMPLE_SOURCES_DIR}]

    state = await run_agent(sources)

    results = [
        AgentItemResult(
            source=item.get("source", ""),
            label=item.get("label", ""),
            verdict=Verdict(item.get("verdict", "safe")),
            attackType=item.get("attack_type"),
            reason=item.get("reason", ""),
            confidence=item.get("confidence", 0.0),
            action=item.get("action", ""),
            blocked=item.get("blocked", False),
        )
        for item in state.get("results", [])
    ]

    return AgentRunResponse(
        summary=AgentSummary(**state.get("summary", {})),
        results=results,
        errors=state.get("errors", []),
    )
