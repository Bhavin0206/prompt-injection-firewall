"""Smoke test for the agent graph (Way 2 - Tasks 3, 7 & 8).

Runs the graph against the sample folder and checks that items were fetched
(fetch node) and scanned (scan node) with the expected verdicts.

Run from the backend folder:
    .\\.venv\\Scripts\\python.exe scripts\\check_agent_graph.py
"""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.domain.agents.graph import agent_graph  # noqa: E402
from app.domain.agents.state import initial_state  # noqa: E402

SAMPLES = Path(__file__).resolve().parents[1] / "data" / "sample_sources"

# What we expect per sample file
EXPECTED = {
    "email_malicious.eml": "blocked",
    "support_ticket.txt": "blocked",
    "product_page.html": "blocked",
    "deploy_script.py": "blocked",
    "email_safe.eml": "safe",
    "meeting_notes.txt": "safe",
}


async def main() -> int:
    passed = 0
    total = 0

    state = initial_state([{"type": "folder", "value": str(SAMPLES)}])
    result = await agent_graph.ainvoke(state)

    items = result.get("items", [])
    results = result.get("results", [])
    print(f"fetched {len(items)} item(s), scanned {len(results)}\n")
    for r in results:
        print(f"  {r['verdict']:7} | {r['label']:24} | "
              f"action={r.get('action','?'):5} | blocked={r.get('blocked')} | "
              f"{r.get('attack_type') or '-':20} | {r['confidence']}%")

    # 1. every item was scanned
    total += 1
    ok = len(results) == len(items) == len(EXPECTED)
    passed += ok
    print(f"\n[{'PASS' if ok else 'FAIL'}] all {len(EXPECTED)} items fetched + scanned")

    # 2. verdicts match expectations
    total += 1
    by_label = {r["label"]: r["verdict"] for r in results}
    ok = all(by_label.get(label) == expected for label, expected in EXPECTED.items())
    passed += ok
    print(f"[{'PASS' if ok else 'FAIL'}] verdicts match expectations")

    # 3. results carry the fields the dashboard needs
    total += 1
    ok = all(
        {"source", "label", "verdict", "confidence"} <= set(r.keys())
        for r in results
    )
    passed += ok
    print(f"[{'PASS' if ok else 'FAIL'}] results have the dashboard fields")

    # 4. no errors
    total += 1
    ok = not result.get("errors")
    passed += ok
    print(f"[{'PASS' if ok else 'FAIL'}] no errors (got: {result.get('errors')})")

    # 5. decide node: every result has action + blocked + a message
    total += 1
    ok = all(
        r.get("action") and "blocked" in r and r.get("reason")
        for r in results
    )
    passed += ok
    print(f"[{'PASS' if ok else 'FAIL'}] decide node set action + blocked + reason")

    # 6. blocked verdicts -> blocked True + action block/flag ; safe -> pass
    total += 1
    ok = all(
        (r["blocked"] and r["action"] in {"block", "flag"})
        if r["verdict"] == "blocked"
        else (not r["blocked"] and r["action"] == "pass")
        for r in results
    )
    passed += ok
    print(f"[{'PASS' if ok else 'FAIL'}] actions match verdicts")

    # 7. summarize node produced the dashboard counts
    summary = result.get("summary", {})
    exp_blocked = sum(1 for v in EXPECTED.values() if v == "blocked")
    exp_safe = sum(1 for v in EXPECTED.values() if v == "safe")
    print(f"\nsummary: {summary}")
    total += 1
    ok = (
        summary.get("fetched") == len(EXPECTED)
        and summary.get("blocked") == exp_blocked
        and summary.get("passed") == exp_safe
        and "flagged" in summary
        and "errors" in summary
    )
    passed += ok
    print(f"[{'PASS' if ok else 'FAIL'}] summary counts "
          f"(fetched {len(EXPECTED)} / blocked {exp_blocked} / passed {exp_safe})")

    print(f"\n{passed}/{total} passed")
    return 0 if passed == total else 1


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
