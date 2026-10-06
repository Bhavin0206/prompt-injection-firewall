"""Smoke test for the agent runner (Way 2 - Task 11).

Run from the backend folder:
    .\\.venv\\Scripts\\python.exe scripts\\check_agent_runner.py
"""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.domain.agents.runner import run_agent  # noqa: E402

SAMPLES = Path(__file__).resolve().parents[1] / "data" / "sample_sources"


async def main() -> int:
    state = await run_agent([{"type": "folder", "value": str(SAMPLES)}])

    summary = state.get("summary", {})
    results = state.get("results", [])

    print("run_agent finished")
    print("summary:", summary)
    for r in results:
        print(f"  {r['verdict']:7} | {r['label']:24} | action={r.get('action')}")

    ok = (
        summary.get("fetched") == len(results)
        and len(results) >= 4
        and summary.get("blocked", 0) >= 2
        and summary.get("passed", 0) >= 2
    )
    print(f"\n[{'PASS' if ok else 'FAIL'}] runner returned the expected state")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
