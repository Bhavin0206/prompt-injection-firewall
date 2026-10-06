"""Smoke test for the folder / email tool (Way 2 - Task 5).

Reads backend/data/sample_sources and reports what was found.

Run from the backend folder:
    .\\.venv\\Scripts\\python.exe scripts\\check_read_files.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.domain.agents.tools.read_files import ReadError, read_folder  # noqa: E402

SAMPLES = Path(__file__).resolve().parents[1] / "data" / "sample_sources"

EXPECTED_FILES = {
    "email_malicious.eml",
    "email_safe.eml",
    "meeting_notes.txt",
    "support_ticket.txt",
    "product_page.html",
    "deploy_script.py",
}


def main() -> int:
    passed = 0
    total = 0

    items = read_folder(SAMPLES)
    print(f"read {len(items)} item(s) from {SAMPLES.name}/\n")
    for item in items:
        print(f"  - {item['label']:24} ({len(item['content'])} chars)")

    labels = {item["label"] for item in items}

    # 1. every expected sample file was read
    total += 1
    ok = EXPECTED_FILES <= labels
    passed += ok
    print(f"\n[{'PASS' if ok else 'FAIL'}] all expected sample files read "
          f"(missing: {EXPECTED_FILES - labels or 'none'})")

    # 2. the malicious email kept its body text
    total += 1
    malicious = next((i for i in items if i["label"] == "email_malicious.eml"), None)
    ok = bool(malicious) and "IGNORE ALL PREVIOUS INSTRUCTIONS" in malicious["content"]
    passed += ok
    print(f"[{'PASS' if ok else 'FAIL'}] malicious email body extracted")

    # 3. .eml Subject line captured
    total += 1
    ok = bool(malicious) and malicious["content"].startswith("Subject: Vendor invoice")
    passed += ok
    print(f"[{'PASS' if ok else 'FAIL'}] email subject captured")

    # 4. HTML is converted to plain text (hidden div still readable)
    total += 1
    page = next((i for i in items if i["label"] == "product_page.html"), None)
    ok = bool(page) and "ignore all previous instructions" in page["content"].lower()
    passed += ok
    print(f"[{'PASS' if ok else 'FAIL'}] html converted to text (hidden text kept)")

    # 5. missing folder raises ReadError
    total += 1
    try:
        read_folder(SAMPLES / "does-not-exist")
        print("[FAIL] missing folder did not raise")
    except ReadError:
        passed += 1
        print("[PASS] missing folder raises ReadError")

    print(f"\n{passed}/{total} passed")
    return 0 if passed == total else 1


if __name__ == "__main__":
    raise SystemExit(main())
