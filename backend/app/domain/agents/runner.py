"""Agent runner — thin wrapper that invokes the agent graph (Way 2).

One call = one agent pass over the given sources:
    run_agent(sources) -> final AgentState (items, results, summary, errors)

The API layer and tests call this; they never touch the graph directly.
"""

from __future__ import annotations

from app.domain.agents.graph import agent_graph
from app.domain.agents.state import AgentState, SourceSpec, initial_state


async def run_agent(sources: list[SourceSpec]) -> AgentState:
    """Run one agent pass and return the final graph state."""
    return await agent_graph.ainvoke(initial_state(sources))
