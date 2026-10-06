"""Error-handling test for the agent (Way 2 - Task 13).

A failing source must NOT break the run: the good source is still fetched and
scanned, and each failure is reported in `errors` / `summary.errors`.

Run from the backend folder:
    .\\.venv\\Scripts\\python.exe scripts\\check_agent_errors.py
"""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.domain.agents.runner import run_agent  # noqa: E402

SAMPLES = Path(__file__).resolve().parents[1] / "data" / "sample_sources"


async def main() -> int:
    state = await run_agent(
        [
            {"type": "folder", "value": str(SAMPLES)},          # good
            {"type": "folder", "value": "C:/does/not/exist"},   # bad folder
            {"type": "url", "value": "https://no-such-host.invalid/"},  # bad url
            {"type": "weird", "value": "x"},                    # unknown type
        ]
    )

    summary = state.get("summary", {})
    errors = state.get("errors", [])
    items = state.get("items", [])

    print(f"items fetched : {len(items)}  (expected 4 from the good folder)")
    print(f"errors        : {len(errors)}")
    for err in errors:
        print(f"   - {err[:100]}")
    print(f"summary       : {summary}")

    passed = 0
    total = 0

    # 1. the good source was still fetched + scanned
    total += 1
    ok = len(items) >= 4 and len(state.get("results", [])) == len(items)
    passed += ok
    print(f"\n[{'PASS' if ok else 'FAIL'}] good source still processed (not aborted)")

    # 2. the three bad sources were reported
    total += 1
    ok = len(errors) == 3
    passed += ok
    print(f"[{'PASS' if ok else 'FAIL'}] 3 failing sources reported")

    # 3. summary counts the errors
    total += 1
    ok = summary.get("errors") == 3 and summary.get("fetched") == len(items)
    passed += ok
    print(f"[{'PASS' if ok else 'FAIL'}] summary.errors == 3 and fetched == {len(items)}")

    print(f"\n{passed}/{total} passed")
    return 0 if passed == total else 1


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
